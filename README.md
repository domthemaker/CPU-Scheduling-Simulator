# CPU Scheduling Simulator — PT 101

CustomTkinter desktop simulator for FCFS, non-preemptive SJF, preemptive SRTF, and Round Robin.

## Run

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Project modules
- `main.py`: app entry point
- `gui.py`: Flame Orange interface, Gantt chart, metrics, comparison dashboard
- `theme.py`: colors, algorithm names, tooltip descriptions
- `process.py`: optional typed process model (the GUI currently uses tuples for compatibility)
- `utils.py`: process input validation
- `algorithms/`: one scheduling implementation per algorithm, plus shared segment/metrics helpers
- `tests/test_scheduling.py`: regression checks


## Features

- Add and manage processes with Process ID, Arrival Time, and Burst Time.
- Simulate four CPU scheduling algorithms:
  - First Come, First Served (FCFS)
  - Shortest Job First (SJF) – Non-Preemptive
  - Shortest Remaining Time First (SRTF) – Preemptive
  - Round Robin (RR)
- Display Gantt charts to visualize process execution.
- Calculate Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT), and Response Time (RT).
- Display average Turnaround Time, Waiting Time, and Response Time.
- Compare scheduling algorithms using tables and charts.
- Run all four algorithms for the same set of processes.

## Documentation

The following documents are available in the `docs` folder:

- [User Guide](docs/User_Guide.pdf) – Instructions for installing, running, and using the simulator.
- [Testing Report](docs/Testing_Report.pdf) – Test cases with expected and actual results.

## Testing

The project includes automated tests to check the correctness of the CPU scheduling algorithms.

To run the tests, open a terminal in the project folder and enter:

```bash
python -m unittest discover -s tests
```

The tests check the scheduling results against expected outputs to help verify that the algorithms work correctly.
