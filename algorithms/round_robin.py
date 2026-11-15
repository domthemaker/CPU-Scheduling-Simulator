from .common import prepare, add_segment, finalize

from collections import deque

def run(processes, quantum=3):
    jobs = prepare(processes)
    time, segments, finished = 0, [], 0
    def add(pid, start, end):
        add_segment(segments, pid, start, end)
    arrivals = sorted(jobs, key=lambda j: (j['at'], j['order']))
    queue, idx = deque(), 0
    while finished < len(jobs):
        while idx < len(jobs) and arrivals[idx]['at'] <= time:
            queue.append(arrivals[idx]); idx += 1
        if not queue:
            nxt = arrivals[idx]['at']
            add('IDLE', time, nxt); time = nxt
            continue
        job = queue.popleft()
        if job['first'] is None:
            job['first'] = time
        duration = min(quantum, job['left'])
        add(job['pid'], time, time + duration)
        time += duration; job['left'] -= duration
        while idx < len(jobs) and arrivals[idx]['at'] <= time:
            queue.append(arrivals[idx]); idx += 1
        if job['left']:
            queue.append(job)
        else:
            job['ct'] = time; finished += 1
    return finalize(jobs, segments)
