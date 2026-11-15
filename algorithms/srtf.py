from .common import prepare, add_segment, finalize

def run(processes, quantum=3):
    jobs = prepare(processes)
    time, segments, finished = 0, [], 0
    def add(pid, start, end):
        add_segment(segments, pid, start, end)
    while finished < len(jobs):
        ready = [j for j in jobs if j['left'] > 0 and j['at'] <= time]
        if not ready:
            nxt = min(j['at'] for j in jobs if j['left'] > 0)
            add('IDLE', time, nxt); time = nxt
            continue
        job = min(ready, key=lambda j: (j['left'], j['at'], j['order']))
        if job['first'] is None:
            job['first'] = time
        add(job['pid'], time, time + 1)
        job['left'] -= 1; time += 1
        if not job['left']:
            job['ct'] = time; finished += 1
    return finalize(jobs, segments)
