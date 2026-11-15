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

