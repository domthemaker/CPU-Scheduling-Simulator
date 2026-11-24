# CPU Scheduling Simulator — PT 101

A modular Python console simulator for FCFS, non-preemptive SJF, preemptive SRTF, and Round Robin (Topic 2).

## Run

Requires Python 3; no external dependencies.

```bash
python main.py
```

Select an algorithm, enter a positive time quantum if using Round Robin or comparison, then enter the process count, unique IDs, nonnegative arrival times and positive burst times. Each simulation uses fresh input; comparison uses one input set for all four algorithms. Processes are not saved to disk.

## Output

Each algorithm displays PID, AT, BT, CT, TAT, WT, RT, a text Gantt chart and averages. Round Robin also displays the quantum and each execution slice with remaining burst time. Comparison displays all four results followed by a summary; an asterisk marks each lowest average.

TAT = CT - AT; WT = TAT - BT; RT = first start - AT. Ties use arrival order then input order. Round Robin admits new arrivals before requeuing the running process. Every RR slice is displayed separately.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover differing arrivals, CPU idle periods, simultaneous arrivals, Round Robin slices and invalid inputs.

## Source organization

`main.py` handles navigation; `utils.py` handles input; `display.py` formats results; `algorithms/` contains the four implementations and common calculations; `tests/` contains automated tests.

## Academic disclosure

AI assistance was used to revise the source code and tests. Group members should review, understand and disclose assistance according to course policy.
