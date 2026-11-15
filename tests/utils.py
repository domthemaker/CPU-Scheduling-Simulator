
def valid_process(pid, arrival, burst, existing):
    return bool(pid) and arrival >= 0 and burst > 0 and all(p[0] != pid for p in existing)
