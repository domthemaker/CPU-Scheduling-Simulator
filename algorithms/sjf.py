from .common import prepare, record, results


def run(processes):
    pending = prepare(processes)
    time = 0
    first, finish, chart = {}, {}, []
    while pending:
        ready = [p for p in pending if p.arrival <= time]
        if not ready:
            record(chart, 'IDLE', time, pending[0].arrival)
            time = pending[0].arrival
            continue
        p = min(ready, key=lambda p: p.burst)
        pending.remove(p)
        first[p.pid] = time
        record(chart, p.pid, time, time + p.burst)
        time += p.burst
        finish[p.pid] = time
    return results(processes, first, finish, chart)
