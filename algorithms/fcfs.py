from .common import prepare, add_segment, finalize

def run(processes, quantum=3):
    jobs = prepare(processes)
    time, segments, finished = 0, [], 0
    def add(pid, start, end):
        add_segment(segments, pid, start, end)
    algorithm = 'FCFS'
    while finished < len(jobs):
        ready = [j for j in jobs if j['ct'] is None and j['at'] <= time]
        if not ready:
            nxt = min(j['at'] for j in jobs if j['ct'] is None)
            add('IDLE', time, nxt); time = nxt
            continue
        key = (lambda j: (j['at'], j['order'])) if algorithm == 'FCFS' else (lambda j: (j['bt'], j['at'], j['order']))
        job = min(ready, key=key)
        job['first'] = time
        add(job['pid'], time, time + job['bt'])
        time += job['bt']; job['ct'] = time; finished += 1
    return finalize(jobs, segments)
