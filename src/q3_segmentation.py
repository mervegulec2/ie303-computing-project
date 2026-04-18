#!/usr/bin/env python3
"""
Q3: Image Segmentation Using IP
Performs image segmentation using optimization techniques.
"""

import numpy as np
from PIL import Image
from gurobipy import Model, GRB, quicksum
import os


def load_image(image_path):
    """
    Load image from file and return as numpy array.

    Args:
        image_path: Path to the image file

    Returns:
        Numpy array of shape (height, width, 3) with RGB values
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path)
    img_array = np.array(img)

    # Ensure RGB format
    if len(img_array.shape) == 2:
        # Grayscale to RGB
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:
        # RGBA to RGB
        img_array = img_array[:, :, :3]

    return img_array


def chebyshev_distance(color1, color2):
    """
    Calculate Chebyshev distance (L∞ norm) between two RGB colors.

    d(x,y) = max_i |x_i - y_i|

    Args:
        color1: RGB tuple/array (0-255)
        color2: RGB tuple/array (0-255)

    Returns:
        Chebyshev distance
    """
    return max(abs(int(c1) - int(c2)) for c1, c2 in zip(color1, color2))


def custom_foreground_penalty(pixel_color, bg_color, distance_func, image_shape):
    """
    Custom foreground penalty function.
    High when pixel is close to background, low when distant.

    Uses exponential decay based on normalized distance.

    Args:
        pixel_color: RGB values of pixel
        bg_color: RGB values of background
        distance_func: Distance function
        image_shape: (height, width) for normalization

    Returns:
        Foreground penalty value
    """
    distance = distance_func(pixel_color, bg_color)
    max_possible_distance = distance_func([0, 0, 0], [255, 255, 255])  # 255

    # Normalize distance to [0, 1]
    normalized_dist = distance / max_possible_distance

    # Exponential penalty: high when close to BG, low when far
    # f = 100 * exp(-5 * d) + 10 * (1 - d)
    penalty = 100 * np.exp(-5 * normalized_dist) + 10 * (1 - normalized_dist)

    return penalty


def custom_background_penalty(pixel_color, bg_color, distance_func, image_shape):
    """
    Custom background penalty function.
    High when pixel is distant from background, low when close.

    Uses quadratic penalty based on distance.

    Args:
        pixel_color: RGB values of pixel
        bg_color: RGB values of background
        distance_func: Distance function
        image_shape: (height, width) for normalization

    Returns:
        Background penalty value
    """
    distance = distance_func(pixel_color, bg_color)
    max_possible_distance = distance_func([0, 0, 0], [255, 255, 255])  # 255

    # Normalize distance to [0, 1]
    normalized_dist = distance / max_possible_distance

    # Quadratic penalty: low when close to BG, high when far
    # b = 50 * d^2 + 5 * d
    penalty = 50 * (normalized_dist ** 2) + 5 * normalized_dist

    return penalty


def custom_smoothness_penalty(color1, color2, distance_func):
    """
    Custom smoothness penalty function.
    High when colors are similar, low when different.

    Uses Gaussian kernel based on color difference.

    Args:
        color1: RGB values of first pixel
        color2: RGB values of second pixel
        distance_func: Distance function

    Returns:
        Smoothness penalty value
    """
    distance = distance_func(color1, color2)
    max_possible_distance = distance_func([0, 0, 0], [255, 255, 255])  # 255

    # Normalize distance to [0, 1]
    normalized_dist = distance / max_possible_distance

    # Gaussian penalty: high when colors are similar (small distance)
    # s = 30 * exp(-2 * d^2) + 2 * (1 - d)
    penalty = 30 * np.exp(-2 * (normalized_dist ** 2)) + 2 * (1 - normalized_dist)

    return penalty


def get_neighbors(i, j, height, width):
    """
    Get 4-connected neighbors of pixel (i,j).

    Args:
        i, j: Pixel coordinates
        height, width: Image dimensions

    Returns:
        List of (ni, nj) neighbor coordinates
    """
    neighbors = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-connected
        ni, nj = i + di, j + dj
        if 0 <= ni < height and 0 <= nj < width:
            neighbors.append((ni, nj))
    return neighbors


def segment_image_ip(image_array, bg_color, distance_func,
                    foreground_penalty_func, background_penalty_func, smoothness_penalty_func):
    """
    Segment image using Integer Programming.

    Formulation resembles Network Cut / Min-Cut problem.

    Decision Variables:
    - x_{i,j}: Binary variable, 1 if pixel (i,j) is foreground, 0 if background

    Objective: Minimize total penalties
    sum_{i,j} [f_{i,j} * x_{i,j} + b_{i,j} * (1 - x_{i,j})] +
    sum_{(i,j)~(u,v)} s_{(i,j),(u,v)} * |x_{i,j} - x_{u,v}|

    The smoothness term |x_{i,j} - x_{u,v}| can be linearized using:
    |x_a - x_b| = y_{a,b} where y_{a,b} >= x_a - x_b and y_{a,b} >= x_b - x_a

    Args:
        image_array: RGB image array (height, width, 3)
        bg_color: Background color (R, G, B)
        distance_func: Distance function
        foreground_penalty_func: Function to compute f_{i,j}
        background_penalty_func: Function to compute b_{i,j}
        smoothness_penalty_func: Function to compute s_{(i,j),(u,v)}

    Returns:
        Binary segmentation mask (height, width)
    """
    height, width = image_array.shape[:2]

    print(f"Image size: {width}×{height} = {height*width} pixels")
    print(f"Total variables: {height*width} binary + smoothness variables")

    # Create model
    model = Model("Image_Segmentation")
    model.setParam('OutputFlag', 0)  # Suppress output
    model.setParam('TimeLimit', 300)  # 5 minute time limit

    # Decision variables: x[i,j] = 1 if foreground, 0 if background
    x = {}
    for i in range(height):
        for j in range(width):
            x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Smoothness variables: y[i,j,u,v] = |x[i,j] - x[u,v]|
    # We linearize |a - b| using y >= a - b and y >= b - a
    y = {}
    for i in range(height):
        for j in range(width):
            for ni, nj in get_neighbors(i, j, height, width):
                if (i, j) < (ni, nj):  # Avoid duplicates
                    y[i, j, ni, nj] = model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1,
                                                  name=f"y_{i}_{j}_{ni}_{nj}")

    # Precompute penalties
    print("Precomputing penalties...")
    f_penalties = {}
    b_penalties = {}
    s_penalties = {}

    for i in range(height):
        for j in range(width):
            pixel_color = image_array[i, j]
            f_penalties[i, j] = foreground_penalty_func(pixel_color, bg_color, distance_func, (height, width))
            b_penalties[i, j] = background_penalty_func(pixel_color, bg_color, distance_func, (height, width))

            # Smoothness penalties for neighbors
            for ni, nj in get_neighbors(i, j, height, width):
                if (i, j) < (ni, nj):  # Compute once per edge
                    color1 = image_array[i, j]
                    color2 = image_array[ni, nj]
                    s_penalties[i, j, ni, nj] = smoothness_penalty_func(color1, color2, distance_func)

    # Objective function
    print("Building objective function...")
    objective = 0

    # Unary terms: foreground and background penalties
    for i in range(height):
        for j in range(width):
            objective += f_penalties[i, j] * x[i, j]  # Foreground penalty
            objective += b_penalties[i, j] * (1 - x[i, j])  # Background penalty

    # Smoothness terms
    for i in range(height):
        for j in range(width):
            for ni, nj in get_neighbors(i, j, height, width):
                if (i, j) < (ni, nj):
                    objective += s_penalties[i, j, ni, nj] * y[i, j, ni, nj]

    model.setObjective(objective, GRB.MINIMIZE)

    # Constraints for smoothness variables
    print("Adding smoothness constraints...")
    for i in range(height):
        for j in range(width):
            for ni, nj in get_neighbors(i, j, height, width):
                if (i, j) < (ni, nj):
                    # y >= x[i,j] - x[ni,nj]
                    model.addConstr(y[i, j, ni, nj] >= x[i, j] - x[ni, nj])
                    # y >= x[ni,nj] - x[i,j]
                    model.addConstr(y[i, j, ni, nj] >= x[ni, nj] - x[i, j])

    # Solve
    print("Solving IP model...")
    model.optimize()

    if model.status != GRB.OPTIMAL:
        print(f"Warning: Model status = {model.status}")
        if model.status == GRB.TIME_LIMIT:
            print("Time limit reached, using best solution found")
        elif model.status != GRB.SUBOPTIMAL:
            raise RuntimeError("IP model did not solve optimally")

    # Extract solution
    segmentation = np.zeros((height, width), dtype=int)
    for i in range(height):
        for j in range(width):
            segmentation[i, j] = 1 if x[i, j].X > 0.5 else 0

    return segmentation


def calculate_iou(pred_mask, true_mask):
    """
    Calculate Intersection over Union (IoU).

    IoU = |pred ∩ true| / |pred ∪ true|

    Args:
        pred_mask: Predicted binary mask
        true_mask: Ground truth binary mask

    Returns:
        IoU score (0.0 to 1.0)
    """
    pred_mask = pred_mask.astype(bool)
    true_mask = true_mask.astype(bool)

    intersection = np.logical_and(pred_mask, true_mask).sum()
    union = np.logical_or(pred_mask, true_mask).sum()

    if union == 0:
        return 1.0 if intersection == 0 else 0.0

    return intersection / union


def save_segmentation_mask(mask, output_path):
    """
    Save segmentation mask as image.

    Args:
        mask: Binary mask array
        output_path: Output file path
    """
    # Convert to PIL Image (0=black, 255=white)
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    mask_img.save(output_path)
    print(f"Segmentation mask saved to: {output_path}")


def main():
    """Main function for Q3"""
    print("Q3: Image Segmentation Using IP")
    print("=" * 40)

    # Choose unique combination for bonus points
    print("🎯 UNIQUE COMBINATION (for 5 bonus points):")
    print("- Background Color: White (255, 255, 255)")
    print("- Distance Metric: Chebyshev Distance (L∞ norm)")
    print("- Foreground Penalty: Exponential decay + linear term")
    print("- Background Penalty: Quadratic + linear term")
    print("- Smoothness Penalty: Gaussian kernel")
    print()

    # Parameters
    bg_color = (255, 255, 255)  # White background
    distance_func = chebyshev_distance

    # Image selection - let's use the white background image
    image_path = "data/images/white.png"
    print(f"Loading image: {image_path}")

    try:
        image_array = load_image(image_path)
        height, width = image_array.shape[:2]
        print(f"Image loaded: {width}×{height} pixels")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Segment image
    print("\nSegmenting image using IP...")
    try:
        segmentation = segment_image_ip(
            image_array=image_array,
            bg_color=bg_color,
            distance_func=distance_func,
            foreground_penalty_func=custom_foreground_penalty,
            background_penalty_func=custom_background_penalty,
            smoothness_penalty_func=custom_smoothness_penalty
        )
    except Exception as e:
        print(f"Error in segmentation: {e}")
        return

    # Save result
    output_path = "results/segmentation_mask.png"
    save_segmentation_mask(segmentation, output_path)

    # Calculate IoU (we don't have ground truth, so we'll simulate)
    print("\nIoU Calculation:")
    print("Note: Since we don't have ground truth mask, we'll demonstrate")
    print("the IoU calculation with a simulated ground truth.")

    # For demonstration, create a simple ground truth
    # Assume foreground is the "soldier" part - let's say non-white pixels
    simulated_gt = np.any(image_array < 250, axis=2).astype(int)  # Non-white pixels

    iou_score = calculate_iou(segmentation, simulated_gt)
    print(".4f")

    # Save IoU result
    with open("results/iou.txt", "w") as f:
        f.write(f"IoU Score: {iou_score:.4f}\n")
        f.write("Note: This is calculated against simulated ground truth\n")
        f.write("(non-white pixels assumed to be foreground)\n")

    print("\n" + "="*40)
    print("PENALTY FUNCTIONS EXPLANATION")
    print("="*40)
    print("Foreground Penalty f(i,j):")
    print("  High when pixel close to background → encourages background labeling")
    print("  Formula: 100*exp(-5*d) + 10*(1-d)")
    print()
    print("Background Penalty b(i,j):")
    print("  High when pixel far from background → encourages foreground labeling")
    print("  Formula: 50*d² + 5*d")
    print()
    print("Smoothness Penalty s(i,j,u,v):")
    print("  High when neighboring pixels have similar colors")
    print("  → discourages cutting between similar regions")
    print("  Formula: 30*exp(-2*d²) + 2*(1-d)")

    print("\n" + "="*40)
    print("GIGO PRINCIPLE EXPLANATION")
    print("="*40)
    print("Even with 0.00% optimality gap, IoU < 1.0 because:")
    print("1. Distance metric choice affects color similarity perception")
    print("2. Penalty functions may not perfectly capture 'foreground-ness'")
    print("3. IP finds mathematical optimum, but problem may be ill-posed")
    print("4. No penalty function perfectly models human perception")
    print("5. Color space quantization and noise affect boundary detection")


if __name__ == "__main__":
    main()
