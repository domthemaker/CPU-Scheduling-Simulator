# Shortest Job First (non-preemptive scheduling).

from .common import prepare, record, results


def run(processes):
    pending = prepare(processes)
    time = 0
    first, finish, chart = {}, {}, []
    # Continue until every pending process has finished.
    while pending:
        # Consider only processes that have already arrived.
        ready = [p for p in pending if p.arrival <= time]
        # If none are ready, advance to the next arrival.
        if not ready:
            record(chart, 'IDLE', time, pending[0].arrival)
            time = pending[0].arrival
            continue
        # Choose the ready process with the shortest burst time.
        p = min(ready, key=lambda p: p.burst)
        pending.remove(p)
        # Run the chosen process to completion without interruption.
        first[p.pid] = time
        record(chart, p.pid, time, time + p.burst)
        time += p.burst
        finish[p.pid] = time
    return results(processes, first, finish, chart)
