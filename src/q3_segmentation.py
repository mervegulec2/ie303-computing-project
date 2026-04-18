#!/usr/bin/env python3
"""
Q3: Image Segmentation
Performs image segmentation using optimization techniques.
"""

import numpy as np
from PIL import Image


def load_image(image_path):
    """Load image from file"""
    return np.array(Image.open(image_path))


def segment_image(image_array):
    """Segment image using optimization"""
    # TODO: Implement Q3 solution
    pass


def calculate_iou(mask1, mask2):
    """Calculate Intersection over Union (IoU)"""
    intersection = np.logical_and(mask1, mask2).sum()
    union = np.logical_or(mask1, mask2).sum()
    return intersection / union if union > 0 else 0


def solve_segmentation_problem():
    """Main segmentation solving function"""
    # TODO: Implement Q3 solution
    pass


if __name__ == "__main__":
    solve_segmentation_problem()
