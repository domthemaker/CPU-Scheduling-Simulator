# Round Robin scheduling using a ready queue and a fixed time quantum.

from collections import deque
from .common import prepare, record, results


def run(processes, quantum):
    # A time quantum must be a positive integer for console inputs.
    if quantum < 1:
        raise ValueError('Quantum must be positive.')
    # Keep incoming processes in arrival order and track their remaining bursts.
    pending = deque(prepare(processes))
    remaining = {p.pid: p.burst for p in pending}
    ready = deque()
    time = 0
    first, finish, chart = {}, {}, []
    trace = []
    # Continue while processes are waiting to arrive or ready to execute.
    while pending or ready:
        # Move newly arrived processes into the ready queue.
        while pending and pending[0].arrival <= time:
            ready.append(pending.popleft())
        # If the ready queue is empty, advance to the next arrival.
        if not ready:
            end = pending[0].arrival
            record(chart, 'IDLE', time, end)
            time = end
            continue
        # Take the process at the front of the queue.
        p = ready.popleft()
        # Record its first start time only once.
        first.setdefault(p.pid, time)
        # Execute for at most one quantum, or until the process finishes.
        duration = min(quantum, remaining[p.pid])
        # Keep each time slice separate in the Gantt chart.
        chart.append((p.pid, time, time + duration))
        time += duration
        remaining[p.pid] -= duration
        # Record the executed and remaining time for this slice.
        trace.append((len(trace) + 1, p.pid, time - duration, time,
                      duration, remaining[p.pid]))
        # Queue new arrivals before returning the unfinished process to the queue.
        while pending and pending[0].arrival <= time:
            ready.append(pending.popleft())
        # Requeue unfinished processes; otherwise record completion time.
        if remaining[p.pid]:
            ready.append(p)
        else:
            finish[p.pid] = time
    # Calculate the final metrics and return the execution trace.
    rows, chart = results(processes, first, finish, chart)
    return rows, chart, trace
