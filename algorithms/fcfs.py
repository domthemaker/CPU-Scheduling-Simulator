from .common import prepare, record, results


def run(processes):
    time = 0
    first, finish, chart = {}, {}, []
    for p in prepare(processes):
        if time < p.arrival:
            record(chart, 'IDLE', time, p.arrival)
            time = p.arrival
        first[p.pid] = time
        record(chart, p.pid, time, time + p.burst)
        time += p.burst
        finish[p.pid] = time
    return results(processes, first, finish, chart)
