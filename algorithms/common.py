# Shared validation, timeline recording and metric calculations.

# Validate process data before running an algorithm.
def prepare(processes):
    if not processes:
        raise ValueError('Add at least one process.')
    if len({p.pid for p in processes}) != len(processes):
        raise ValueError('Duplicate process IDs.')
    if any(not p.pid.strip() or p.pid.upper() == 'IDLE' or p.arrival < 0 or p.burst < 1 for p in processes):
        raise ValueError('Invalid process.')
    # Sort by arrival time, preserving input order for equal arrivals.
    return sorted(processes, key=lambda p: p.arrival)


# Record an execution interval in the Gantt chart.
def record(chart, pid, start, end):
    # Merge consecutive intervals belonging to the same process.
    if chart and chart[-1][0] == pid and chart[-1][2] == start:
        chart[-1] = (pid, chart[-1][1], end)
    else:
        chart.append((pid, start, end))


# Build the result rows in the original input order.
def results(processes, first, finish, chart):
    rows = []
    for p in processes:
        ct = finish[p.pid]
        # Turnaround time is completion time minus arrival time.
        tat = ct - p.arrival
        # Waiting time is turnaround minus burst; response time is first start minus arrival.
        rows.append((p.pid, p.arrival, p.burst, ct, tat,
                     tat - p.burst, first[p.pid] - p.arrival))
    return rows, chart


# Calculate the mean turnaround, waiting and response times.
def averages(rows):
    return tuple(sum(r[i] for r in rows) / len(rows) for i in (4, 5, 6))
