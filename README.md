# ICT-4204 — Mobile and Cellular Communication Laboratory

Department of Information and Communication Technology  
Islamic University, Kushtia, Bangladesh

This repository contains nine Python/Jupyter Notebook laboratory experiments based on the official ICT-4204 practical experiment assignment and the corresponding course materials.

## Experiments

| No. | Experiment | Notebook |
|---:|---|---|
| 01 | Calculation of Doppler Shift and Maximum Mobile Velocity | `EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.ipynb` |
| 02 | Calculation of Co-channel Reuse Distance and Reuse Ratio | `EXP02_Cochannel_Reuse_Distance_and_Reuse_Ratio.ipynb` |
| 03 | Study of Frequency Allocation and Channel Assignment in Cellular Networks | `EXP03_Frequency_Allocation_and_Channel_Assignment.ipynb` |
| 04 | Study and Simulation of GSM Network Architecture | `EXP04_GSM_Network_Architecture.ipynb` |
| 05 | Simulation of Handover Between Two Cellular Cells | `EXP05_Cell_Handover_Simulation.ipynb` |
| 06 | Received Signal Strength-Based Base Station Selection | `EXP06_RSS_Based_Base_Station_Selection.ipynb` |
| 07 | Free-Space Path Loss and Received Power Analysis Using MATLAB — implemented here in Python | `EXP07_Free_Space_Path_Loss_and_Received_Power.ipynb` |
| 08 | Analysis of Cell Coverage, Cell Radius, and Cell Splitting | `EXP08_Cell_Coverage_Radius_and_Cell_Splitting.ipynb` |
| 09 | Cellular Traffic, Channel Capacity, and Erlang-B Blocking Probability Analysis | `EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.ipynb` |

## Notebook Structure

Each notebook contains:

- Aim and objectives
- Theory
- Mathematical representation in LaTeX
- Simple laboratory procedure
- Python implementation
- Numerical results
- Graphs and interpretation
- Discussion and conclusion
- Viva questions with short answers

## Requirements

- Python 3
- NumPy
- Pandas
- Matplotlib
- Jupyter

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Jupyter:

```bash
jupyter notebook
```

Then open a notebook from the `notebooks/` directory.

## Notes

- The models are intentionally educational and simplified for an undergraduate practical laboratory.
- Experiment 7 retains the official MATLAB wording from the assignment, but this repository provides an equivalent Python implementation.
- The notebooks are designed to be readable and explainable during a practical examination rather than overengineered.

## Academic Use

Use the notebooks to understand, reproduce, and explain the experiments. Parameters are placed near the top of each implementation so they can be changed during practice.
