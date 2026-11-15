from . import fcfs, sjf, srtf, round_robin

RUNNERS = {
    'FCFS': fcfs.run,
    'SJF': sjf.run,
    'SRTF': srtf.run,
    'Round Robin': round_robin.run,
}


def schedule(processes, algorithm, quantum=3):
    return RUNNERS[algorithm](processes, quantum)

