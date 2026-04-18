# Group 13 - IE303 Computing Project (Spring 2026)

## Project Overview
This project contains solutions for various computing and optimization problems using Python and Gurobi.

## Project Structure

```
Group13_IE303_S2026_ComputingProject/
├── src/                          # Source code
│   ├── q0_test_gurobi.py        # Test Gurobi installation
│   ├── q1_lcm.py                # LCM calculation problem
│   ├── q2_magnetic.py           # Magnetic field problem
│   ├── q3_segmentation.py       # Image segmentation
│   ├── q4_graph.py              # Water jug - Graph approach
│   ├── q4_dp.py                 # Water jug - DP approach
│   └── q4_gcd.py                # GCD via Integer Programming
│
├── data/                         # Input data
│   ├── images/                  # Test images for segmentation
│   │   ├── blue.png
│   │   ├── green.png
│   │   ├── red.png
│   │   └── white.png
│   └── ground_truth/            # Ground truth masks
│       └── mask.png
│
├── results/                      # Output files
│   ├── segmentation_mask.png    # Segmentation mask output
│   └── iou.txt                  # IoU score
│
├── report/                       # Project report
│   └── report.docx              # Word document report
│
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Questions Covered

1. **Q0**: Gurobi Installation Test
2. **Q1**: LCM (Least Common Multiple)
3. **Q2**: Magnetic Field Optimization
4. **Q3**: Image Segmentation
5. **Q4**: Water Jug Problem + GCD via Integer Programming

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Gurobi Installation
```bash
python src/q0_test_gurobi.py
```

## Running Solutions

### Q1 - LCM
```bash
python src/q1_lcm.py
```

### Q2 - Magnetic Field
```bash
python src/q2_magnetic.py
```

### Q3 - Image Segmentation
```bash
python src/q3_segmentation.py
```

### Q4 - Water Jug & GCD
```bash
python src/q4_graph.py   # Graph-based approach
python src/q4_dp.py      # DP-based approach
python src/q4_gcd.py     # Integer programming approach
```

## Input Data

The `data/` folder contains:
- **images/**: Test images for the segmentation task (blue.png, green.png, red.png, white.png)
- **ground_truth/**: Ground truth masks for validation (mask.png)

## Output Results

Results are saved in the `results/` folder:
- **segmentation_mask.png**: Output mask from Q3 segmentation algorithm
- **iou.txt**: Intersection over Union score for segmentation evaluation

## Dependencies

- **numpy**: Numerical computing
- **Pillow**: Image processing
- **scikit-image**: Advanced image operations
- **matplotlib**: Visualization
- **gurobipy**: Gurobi optimization solver
- **pandas**: Data manipulation
- **scipy**: Scientific computing

## Requirements

- Python 3.8+
- Gurobi 9.1+ (requires license)

## Notes

- Ensure Gurobi is properly installed and licensed before running optimization problems
- Test with `q0_test_gurobi.py` first
- Check the `data/` folder for input requirements

## Authors

Group 13 - IE303 Spring 2026
