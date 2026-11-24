from .common import prepare, record, results


def run(processes):
    ordered = prepare(processes)
    remaining = {p.pid: p.burst for p in ordered}
    time = 0
    first, finish, chart = {}, {}, []
    while len(finish) < len(ordered):
        ready = [p for p in ordered if p.arrival <= time and remaining[p.pid] > 0]
        future = [p.arrival for p in ordered if p.arrival > time]
        if not ready:
            end = min(future)
            record(chart, 'IDLE', time, end)
            time = end
            continue
        p = min(ready, key=lambda p: remaining[p.pid])
        first.setdefault(p.pid, time)
        duration = remaining[p.pid]
        if future:
            duration = min(duration, min(future) - time)
        record(chart, p.pid, time, time + duration)
        time += duration
        remaining[p.pid] -= duration
        if remaining[p.pid] == 0:
            finish[p.pid] = time
    return results(processes, first, finish, chart)
