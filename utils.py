
from collections import namedtuple

Process = namedtuple('Process', 'pid arrival burst')


def number(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
        except ValueError:
            pass

        print(f'Enter a whole number of at least {minimum}.')


def read_pid(processes):
    while True:
        pid = input("  Process ID   : ").strip()

        if not pid or not pid.isascii() or not pid.isalnum():
            print("Use letters and numbers only (e.g., P1).")

        elif pid.upper() == "IDLE":
            print("IDLE is reserved for CPU idle time.")

        elif any(p.pid.upper() == pid.upper() for p in processes):
            print("Process ID already exists. Enter a unique ID.")

        else:
            return pid


def read_processes():
    processes = []
    count = number('Enter number of processes: ', 1)

    for i in range(count):
        print(f'\nProcess {i + 1}')

        pid = read_pid(processes)
        arrival = number('  Arrival time : ')
        burst = number('  Burst time   : ', 1)

        processes.append(Process(pid, arrival, burst))

    return processes
