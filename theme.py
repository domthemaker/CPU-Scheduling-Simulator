import customtkinter as ctk
ctk.set_appearance_mode('dark')
BLACK, PANEL, WHITE, ORANGE = '#000000', '#151515', '#FFFFFF', '#FE5101'
MUTED, BORDER, GRAY = '#B8B8B8', '#393939', '#222222'
ORANGE_HOVER, ORANGE_LIGHT = '#D94300', '#FFB380'
COLORS = ['#FE5101', '#E68A42', '#E8B37D', '#C65B35', '#F2A66A', '#B97451']
ALGORITHMS = ['FCFS', 'SJF', 'SRTF', 'Round Robin']
HINTS = {'PID': 'Process ID', 'AT': 'Arrival Time', 'BT': 'Burst Time',
         'CT': 'Completion Time', 'TAT': 'Turnaround Time (CT − AT)',
         'WT': 'Waiting Time (TAT − BT)', 'RT': 'Response Time (first start − AT)',
         'Arrival Time': 'Time the process enters the ready queue',
         'Burst Time': 'Total CPU execution time required'}
