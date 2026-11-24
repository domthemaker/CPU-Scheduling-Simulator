from algorithms import fcfs, sjf, srtf, round_robin
from algorithms.common import averages
from display import heading, show_results, show_comparison
from utils import number, read_processes

ALGORITHMS = [('FCFS', fcfs.run), ('SJF', sjf.run),
              ('SRTF', srtf.run), ('Round Robin', round_robin.run)]


def menu():
    heading('CPU SCHEDULING SIMULATOR')
    print('  1. FCFS (First Come, First Served)')
    print('  2. SJF (Non-preemptive)')
    print('  3. SRTF (Preemptive)')
    print('  4. Round Robin')
    print('  5. Compare All Algorithms')
    print('  0. Exit')
    return input('\nSelect an algorithm: ').strip()


def main():
    while True:
        choice = menu()
        if choice == '0':
            print('Program closed.')
            return
        if choice not in ('1', '2', '3', '4', '5'):
            print('Invalid option. Select 0 to 5.')
            continue

        quantum = number('Time quantum: ', 1) if choice in ('4', '5') else None
        heading('PROCESS INPUT')
        processes = read_processes()
        selected = ALGORITHMS if choice == '5' else [ALGORITHMS[int(choice) - 1]]
        entries = []
        for name, run in selected:
            if name == 'Round Robin':
                rows, chart, trace = run(processes, quantum)
                show_results(name, rows, chart, quantum, trace)
            else:
                rows, chart = run(processes)
                show_results(name, rows, chart)
            entries.append((name, *averages(rows)))
        if choice == '5':
            show_comparison(entries)
        input('\nPress Enter to return to the main menu...')


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print('\nProgram closed.')
