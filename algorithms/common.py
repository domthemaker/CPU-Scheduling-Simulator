def prepare(processes):
    if not processes:
        raise ValueError('Add at least one process.')
    if len({p.pid for p in processes}) != len(processes):
        raise ValueError('Duplicate process IDs.')
    if any(not p.pid.strip() or p.pid.upper() == 'IDLE' or p.arrival < 0 or p.burst < 1 for p in processes):
        raise ValueError('Invalid process.')
    return sorted(processes, key=lambda p: p.arrival)


def record(chart, pid, start, end):
    if chart and chart[-1][0] == pid and chart[-1][2] == start:
        chart[-1] = (pid, chart[-1][1], end)
    else:
        chart.append((pid, start, end))


def results(processes, first, finish, chart):
    rows = []
    for p in processes:
        ct = finish[p.pid]
        tat = ct - p.arrival
        rows.append((p.pid, p.arrival, p.burst, ct, tat,
                     tat - p.burst, first[p.pid] - p.arrival))
    return rows, chart


def averages(rows):
    return tuple(sum(r[i] for r in rows) / len(rows) for i in (4, 5, 6))
