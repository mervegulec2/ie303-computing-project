# IE303 Spring 2026 - Computing Project
## Group 13 Implementation

This repository contains complete implementations for all questions in the IE303 Spring 2026 Computing Project.

## 📋 Project Overview

The project involves solving various optimization problems using Integer Programming (IP) with Gurobi, along with graph algorithms and dynamic programming approaches.

## 🎯 Questions Implemented

### Q0: Gurobi Installation Test
- **File**: `src/q0_test_gurobi.py`
- **Purpose**: Verify Gurobi installation and accessibility
- **Status**: ✅ Complete

### Q1: Least Common Multiple (LCM)
- **File**: `src/q1_lcm.py`
- **Problem**: Compute LCM of a randomly generated set of integers using IP
- **Approach**: IP formulation with divisibility constraints
- **Key Insight**: LCM is the smallest positive integer divisible by all numbers in the set
- **Status**: ✅ Complete and tested

### Q2: Magnetic Field Puzzle
- **File**: `src/q2_magnetic.py`
- **Problem**: Solve a Sudoku-like puzzle where rows and columns must sum to a target value
- **Approach**: IP with binary variables for cell assignments
- **Note**: Waiting for TA Utku to provide the actual puzzle instance
- **Status**: ✅ Framework ready, needs real instance

### Q3: Image Segmentation
- **File**: `src/q3_segmentation.py`
- **Problem**: Segment a 13×20 pixel image using IP
- **Unique Combination** (for 5 bonus points):
  - Background Color: White (255, 255, 255)
  - Distance Metric: Chebyshev Distance (L∞ norm)
  - Foreground Penalty: Exponential decay + linear term
  - Background Penalty: Quadratic + linear term
  - Smoothness Penalty: Gaussian kernel
- **Approach**: Network cut formulation with unary and pairwise terms
- **Status**: ✅ Complete with unique formulation

### Q4: Water Jug Problems
The water jug riddle connects to fundamental number theory concepts:

#### Q4a: Graph-based Solution (Dijkstra)
- **File**: `src/q4_waterjug_graph.py`
- **Problem**: Get exactly 4 gallons using 3L and 5L jugs
- **Approach**: Model as graph search with Dijkstra's algorithm
- **Result**: 6 actions, 294 seconds (under 5-minute bomb timer)
- **Status**: ✅ Complete and optimal

#### Q4b: Dynamic Programming (Value Iteration)
- **File**: `src/q4_waterjug_dp.py`
- **Problem**: Same water jug problem using SSP framework
- **Approach**: Value Iteration for Stochastic Shortest Path
- **Result**: Same optimal solution as Q4a (6 actions, 294 seconds)
- **Status**: ✅ Complete and verified

#### Q4c: GCD via Integer Programming
- **File**: `src/q4_gcd_ip.py`
- **Problem**: Find GCD(976, 1224) using Linear Diophantine Equations
- **Approach**: Bézout's Identity with IP constraints
- **Result**: GCD = 8 with Bézout coefficients x₁=1145, x₂=-913
- **Key Insight**: Water jug problems ≡ Linear Diophantine Equations
- **Status**: ✅ Complete and mathematically verified

## 🔧 Technical Stack

- **Language**: Python 3.9
- **Solver**: Gurobi 12.0.3 (Academic License)
- **Libraries**:
  - `gurobipy`: Integer Programming solver
  - `numpy`: Numerical computations
  - `PIL`: Image processing for Q3
  - `heapq`: Priority queue for Dijkstra
  - `collections`: Data structures

## 📊 Results Summary

| Question | Status | Key Results |
|----------|--------|-------------|
| Q0 | ✅ Complete | Gurobi 12.0.3 installed |
| Q1 | ✅ Complete | LCM computed via IP, matches Python's math.lcm |
| Q2 | ⏳ Ready | Framework complete, waiting for TA instance |
| Q3 | ✅ Complete | IoU = 0.3229, unique penalty functions implemented |
| Q4a | ✅ Complete | 6 actions, 294 seconds (optimal) |
| Q4b | ✅ Complete | Same result as Q4a via DP |
| Q4c | ✅ Complete | GCD(976,1224) = 8 via Diophantine equations |

## 🎯 Key Mathematical Insights

### Water Jug Problems ↔ Number Theory
The water jug riddle is mathematically equivalent to solving Linear Diophantine Equations:
```
a₁×x₁ + a₂×x₂ = b
```
- Solutions exist iff `b` is a multiple of `GCD(a₁,a₂)`
- For 3L and 5L jugs: `GCD(3,5)=1`, so any integer target is achievable
- Each pouring operation corresponds to adding/subtracting jug capacities

### IP for GCD Computation
Using Bézout's Identity: `GCD(a,b)` is the smallest positive integer `d` such that:
```
∃ x,y ∈ ℤ : a×x + b×y = d
```

### Image Segmentation as Network Cut
Formulated as min-cut problem with:
- **Unary terms**: Foreground/background penalties based on color distance
- **Pairwise terms**: Smoothness penalties for neighboring pixels
- **Linearization**: `|x_i - x_j|` constraints using auxiliary variables

## 🚀 Running the Code

```bash
# Test all implementations
cd /path/to/project

# Q0: Test Gurobi
python3 src/q0_test_gurobi.py

# Q1: LCM computation
python3 src/q1_lcm.py

# Q2: Magnetic puzzle (example)
python3 src/q2_magnetic.py

# Q3: Image segmentation
python3 src/q3_segmentation.py

# Q4: Water jug problems
python3 src/q4_waterjug_graph.py   # Dijkstra
python3 src/q4_waterjug_dp.py      # Value Iteration
python3 src/q4_gcd_ip.py           # GCD via IP
```

## 📁 Project Structure

```
Group13_IE303_S2026_ComputingProject/
├── src/
│   ├── q0_test_gurobi.py      # Gurobi installation test
│   ├── q1_lcm.py              # LCM via IP
│   ├── q2_magnetic.py         # Magnetic puzzle framework
│   ├── q3_segmentation.py     # Image segmentation
│   ├── q4_waterjug_graph.py   # Water jug (Dijkstra)
│   ├── q4_waterjug_dp.py      # Water jug (DP)
│   └── q4_gcd_ip.py           # GCD via Diophantine equations
├── data/
│   └── images/
│       ├── white.png          # Q3 test image
│       ├── blue.png
│       ├── green.png
│       └── red.png
├── results/
│   ├── segmentation_mask.png  # Q3 output
│   └── iou.txt               # Q3 IoU score
└── README.md                 # This file
```

## 🎓 Academic Integrity

This implementation is the original work of Group 13 for IE303 Spring 2026. All code is written from scratch with proper understanding of the mathematical formulations and algorithms.

## 📞 Contact

For questions about the implementations or to obtain the magnetic puzzle instance, contact:
- **TA Utku**: For Q2 puzzle instance distribution
- **Group 13**: For implementation details

---

*Last updated: Implementation complete for all questions except Q2 (waiting for TA instance)*
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
python src/q4_waterjug_graph.py   # Graph-based approach
python src/q4_waterjug_dp.py      # DP-based approach
python src/q4_gcd_ip.py           # Integer programming approach
```

## Input Data

The `data/images/` folder contains test images for the segmentation task:
- blue.png
- green.png
- red.png
- white.png
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
