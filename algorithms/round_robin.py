from collections import deque
from .common import prepare, record, results


def run(processes, quantum):
    if quantum < 1:
        raise ValueError('Quantum must be positive.')
    pending = deque(prepare(processes))
    remaining = {p.pid: p.burst for p in pending}
    ready = deque()
    time = 0
    first, finish, chart = {}, {}, []
    trace = []
    while pending or ready:
        while pending and pending[0].arrival <= time:
            ready.append(pending.popleft())
        if not ready:
            end = pending[0].arrival
            record(chart, 'IDLE', time, end)
            time = end
            continue
        p = ready.popleft()
        first.setdefault(p.pid, time)
        duration = min(quantum, remaining[p.pid])
        chart.append((p.pid, time, time + duration))
        time += duration
        remaining[p.pid] -= duration
        trace.append((len(trace) + 1, p.pid, time - duration, time,
                      duration, remaining[p.pid]))
        while pending and pending[0].arrival <= time:
            ready.append(pending.popleft())
        if remaining[p.pid]:
            ready.append(p)
        else:
            finish[p.pid] = time
    rows, chart = results(processes, first, finish, chart)
    return rows, chart, trace
