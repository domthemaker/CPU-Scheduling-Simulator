# Shortest Remaining Time First (preemptive scheduling).

from .common import prepare, record, results


def run(processes):
    ordered = prepare(processes)
    # Track the unfinished burst time of each process.
    remaining = {p.pid: p.burst for p in ordered}
    time = 0
    first, finish, chart = {}, {}, []
    # Repeat until all processes have completed.
    while len(finish) < len(ordered):
        # Identify available unfinished processes and future arrivals.
        ready = [p for p in ordered if p.arrival <= time and remaining[p.pid] > 0]
        future = [p.arrival for p in ordered if p.arrival > time]
        # Advance to the next arrival if the CPU has no ready process.
        if not ready:
            end = min(future)
            record(chart, 'IDLE', time, end)
            time = end
            continue
        # Select the process with the shortest remaining burst.
        p = min(ready, key=lambda p: remaining[p.pid])
        # Keep the original first start time for response time calculation.
        first.setdefault(p.pid, time)
        duration = remaining[p.pid]
        # Stop at the next arrival if it occurs before completion, then reconsider the choice.
        if future:
            duration = min(duration, min(future) - time)
        # Record the interval and deduct the time executed.
        record(chart, p.pid, time, time + duration)
        time += duration
        remaining[p.pid] -= duration
        # Save completion time only when no burst time remains.
        if remaining[p.pid] == 0:
            finish[p.pid] = time
    return results(processes, first, finish, chart)
