# ICT-4204 Mobile and Cellular Communication Laboratory

**Course Title:** Mobile and Cellular Communication Laboratory  
**Course Code:** ICT-4204  
**Department:** Department of Information and Communication Technology  
**University:** Islamic University, Kushtia, Bangladesh

## Repository Overview

This repository contains nine laboratory experiments for ICT-4204. They are based on the official practical experiment assignment and the related course materials. Each experiment comes in two forms:

- a **Jupyter notebook** (the main laboratory document), with theory, equations, implementation, graphs, discussion, and viva questions;
- a **standalone Python script** that runs the same calculations and plots without Jupyter.

## Objectives

- Apply the basic equations of mobile and cellular communication to numerical problems.
- Study frequency reuse, channel assignment, handover, and base-station selection.
- Analyse propagation loss, received power, cell coverage, and cell splitting.
- Evaluate cellular traffic and blocking probability using the Erlang-B model.
- Present results with clear graphs and explain them in a practical examination.

## Tools and Technologies

- Python 3
- NumPy (numerical calculations)
- Pandas (result tables)
- Matplotlib (graphs and diagrams)
- Jupyter Notebook

## Experiments

| Experiment | Title | Notebook | Python Script |
|:---:|---|---|---|
| 01 | Calculation of Doppler Shift and Maximum Mobile Velocity | [EXP01 notebook](notebooks/EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.ipynb) | [EXP01 script](scripts/EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.py) |
| 02 | Calculation of Co-channel Reuse Distance and Reuse Ratio | [EXP02 notebook](notebooks/EXP02_Cochannel_Reuse_Distance_and_Reuse_Ratio.ipynb) | [EXP02 script](scripts/EXP02_Cochannel_Reuse_Distance_and_Reuse_Ratio.py) |
| 03 | Study of Frequency Allocation and Channel Assignment in Cellular Networks | [EXP03 notebook](notebooks/EXP03_Frequency_Allocation_and_Channel_Assignment.ipynb) | [EXP03 script](scripts/EXP03_Frequency_Allocation_and_Channel_Assignment.py) |
| 04 | Study and Simulation of GSM Network Architecture | [EXP04 notebook](notebooks/EXP04_GSM_Network_Architecture.ipynb) | [EXP04 script](scripts/EXP04_GSM_Network_Architecture.py) |
| 05 | Simulation of Handover Between Two Cellular Cells | [EXP05 notebook](notebooks/EXP05_Cell_Handover_Simulation.ipynb) | [EXP05 script](scripts/EXP05_Cell_Handover_Simulation.py) |
| 06 | Received Signal Strength-Based Base Station Selection | [EXP06 notebook](notebooks/EXP06_RSS_Based_Base_Station_Selection.ipynb) | [EXP06 script](scripts/EXP06_RSS_Based_Base_Station_Selection.py) |
| 07 | Free-Space Path Loss and Received Power Analysis Using MATLAB (implemented in Python) | [EXP07 notebook](notebooks/EXP07_Free_Space_Path_Loss_and_Received_Power.ipynb) | [EXP07 script](scripts/EXP07_Free_Space_Path_Loss_and_Received_Power.py) |
| 08 | Analysis of Cell Coverage, Cell Radius, and Cell Splitting | [EXP08 notebook](notebooks/EXP08_Cell_Coverage_Radius_and_Cell_Splitting.ipynb) | [EXP08 script](scripts/EXP08_Cell_Coverage_Radius_and_Cell_Splitting.py) |
| 09 | Cellular Traffic, Channel Capacity, and Erlang-B Blocking Probability Analysis | [EXP09 notebook](notebooks/EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.ipynb) | [EXP09 script](scripts/EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.py) |

## Repository Structure

```text
ICT-4204-LabCodes/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/        # Jupyter notebooks: theory, implementation, results, viva
│   ├── EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.ipynb
│   ├── ...
│   └── EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.ipynb
└── scripts/          # Standalone Python versions of each experiment
    ├── EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.py
    ├── ...
    └── EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.py
```

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

## Environment Setup

Python 3.9 or newer is recommended. Using a virtual environment is optional but keeps dependencies isolated:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Notebooks

```bash
jupyter notebook
```

Then open a notebook from the `notebooks/` directory and choose **Run All**.

## Running the Python Scripts

Run any script from the repository root:

```bash
python scripts/EXP01_Doppler_Shift_and_Maximum_Mobile_Velocity.py
python scripts/EXP09_Cellular_Traffic_Channel_Capacity_and_Erlang_B.py
```

Each script prints its numerical results to the terminal and then opens its graphs in Matplotlib windows. Close the windows to end the script.

## Repository Design

- **Notebooks are the primary laboratory documents.** They explain the theory and show the results inline.
- **Scripts mirror the notebook calculations.** They use the same parameters and equations, so their printed results match the notebooks. They are useful when Jupyter is not available.
- **Parameters are placed at the top** of each notebook implementation and each script, so they can be changed easily during practice.
- **The code is intentionally simple.** It uses plain functions and NumPy/Matplotlib only, so every step can be explained in a viva.

Reference values reproduced by both forms include:

| Experiment | Check | Result |
|:---:|---|---|
| 01 | $f_c = 900$ MHz, $v = 72$ km/h | $f_m \approx 60$ Hz |
| 02 | $N = 7$ | $q = \sqrt{21} \approx 4.583$ |
| 08 | Radius halved, $n = 4$ | $P_{t2}/P_{t1} = 1/16 \approx -12.04$ dB |
| 09 | $A = 78.3$ E, $N = 90$ channels | $B \approx 0.0200$ (2%) |

## Notes

- The models are intentionally educational and simplified for an undergraduate practical laboratory.
- Experiment 7 keeps the official MATLAB wording from the assignment, but this repository provides an equivalent Python implementation.
- The notebooks are designed to be readable and explainable during a practical examination rather than overengineered.

## Academic Use

This repository is intended for academic learning in the ICT-4204 laboratory. Use the notebooks and scripts to understand, reproduce, and explain the experiments. Follow your department's academic integrity rules when using this material for assessed work.
