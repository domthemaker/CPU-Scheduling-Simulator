def prepare(processes):
    return [dict(pid=p[0], at=p[1], bt=p[2], left=p[2], first=None,
                 ct=None, order=i) for i, p in enumerate(processes)]


def add_segment(segments, pid, start, end):
    if start == end:
        return
    if segments and segments[-1][0] == pid and segments[-1][2] == start:
        segments[-1] = (pid, segments[-1][1], end)
    else:
        segments.append((pid, start, end))


def finalize(jobs, segments):
    rows = []
    for j in jobs:
        tat = j['ct'] - j['at']
        wt = tat - j['bt']
        rt = j['first'] - j['at']
        rows.append((j['pid'], j['at'], j['bt'], j['ct'], tat, wt, rt))
    avgs = tuple(sum(row[i] for row in rows) / len(rows) for i in (4, 5, 6))
    return segments, rows, avgs
