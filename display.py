from algorithms.common import averages

WIDTH = 54


def heading(title):
    print('\n' + '=' * WIDTH)
    print(title.center(WIDTH))
    print('=' * WIDTH)


def table(headers, rows):
    data = [list(map(str, headers))] + [list(map(str, row)) for row in rows]
    widths = [max(len(row[i]) for row in data) for i in range(len(headers))]
    border = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'
    print(border)
    for i, row in enumerate(data):
        print('| ' + ' | '.join(v.center(w) for v, w in zip(row, widths)) + ' |')
        if i == 0:
            print(border)
    print(border)


def gantt_chart(chart):
    print('\nGantt Chart')
    for i in range(0, len(chart), 8):
        segments = chart[i:i + 8]
        widths = [max(5, len(pid) + 2, len(str(start))) for pid, start, end in segments]
        border = '+' + '+'.join('-' * w for w in widths) + '+'
        print(border)
        print('|' + '|'.join(s[0].center(w) for s, w in zip(segments, widths)) + '|')
        print(border)
        print(''.join(str(s[1]).ljust(w + 1) for s, w in zip(segments, widths)) + str(segments[-1][2]))


def show_results(name, rows, chart, quantum=None, trace=None):
    heading(name.upper() + ' RESULTS')
    if quantum is not None:
        print(f'Time Quantum: {quantum}\n')
    table(('PID', 'AT', 'BT', 'CT', 'TAT', 'WT', 'RT'), rows)
    gantt_chart(chart)
    if trace is not None:
        print('\nRound Robin Execution Trace')
        table(('Step', 'PID', 'Start', 'End', 'Executed', 'Remaining'), trace)
    tat, wt, rt = averages(rows)
    print(f'\nAverage Turnaround Time : {tat:.2f}')
    print(f'Average Waiting Time    : {wt:.2f}')
    print(f'Average Response Time   : {rt:.2f}')


def show_comparison(entries):
    heading('ALGORITHM COMPARISON')
    best = [min(row[i] for row in entries) for i in (1, 2, 3)]
    rows = [(row[0], *(f'{v:.2f}' + (' *' if v == best[i] else '')
                       for i, v in enumerate(row[1:]))) for row in entries]
    table(('Algorithm', 'Avg TAT', 'Avg WT', 'Avg RT'), rows)
    print('* Indicates the lowest average in each category.')
