# First Come, First Served (non-preemptive scheduling).

from .common import prepare, record, results


def run(processes):
    time = 0
    # Track first start times, completion times and execution intervals.
    first, finish, chart = {}, {}, []
    # Execute processes in arrival order.
    for p in prepare(processes):
        # Record idle time if the next process has not arrived.
        if time < p.arrival:
            record(chart, 'IDLE', time, p.arrival)
            time = p.arrival
        # Run the selected process until its full burst is completed.
        first[p.pid] = time
        record(chart, p.pid, time, time + p.burst)
        time += p.burst
        # Save the completion time for the result calculations.
        finish[p.pid] = time
    return results(processes, first, finish, chart)
