import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from theme import BLACK, PANEL, WHITE, ORANGE, MUTED, BORDER, GRAY, ORANGE_HOVER, ORANGE_LIGHT, COLORS, ALGORITHMS, HINTS
from algorithms import schedule
from utils import valid_process

ctk.set_appearance_mode('dark')


class Studio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('CPU Scheduling Simulator | PT 101')
        self.geometry('1100x850')
        self.minsize(850, 670)
        self.configure(fg_color=BLACK)
        self.processes = [('P1', 0, 6), ('P2', 1, 4), ('P3', 2, 2), ('P4', 3, 5)]
        self.results = {}
        self.active = 'FCFS'
        self.tooltip = None
        self.make_ui()
        self.refresh_processes()
        self.run_all()
    def label(self, parent, text, size=12, color=WHITE, bold=False, **kw):
        return ctk.CTkLabel(parent, text=text, text_color=color,
                            font=('Segoe UI', size, 'bold' if bold else 'normal'), **kw)
    def button(self, parent, text, command, primary=False, width=110):
        return ctk.CTkButton(parent, text=text, command=command, width=width, height=39,
                             corner_radius=4, fg_color=ORANGE if primary else GRAY,
                             hover_color=ORANGE_HOVER if primary else ORANGE,
                             text_color=WHITE, font=('Segoe UI', 14, 'bold'))
    def card(self, parent):
        return ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=4,
                            border_width=1, border_color=BORDER)
    def make_ui(self):
        self.content = ctk.CTkScrollableFrame(self, fg_color=BLACK, corner_radius=0)
        self.content.pack(fill='both', expand=True)
        header = ctk.CTkFrame(self.content, fg_color=BLACK, corner_radius=0, height=84)
        header.pack(fill='x', padx=22, pady=(14, 8))
        self.label(header, 'CPU Scheduling Simulator', 25, WHITE, True).pack(anchor='w')
        self.label(header, 'PT 101  /  PLATFORM TECHNOLOGIES  /  FCFS  /  SJF  /  SRTF  /  ROUND ROBIN',
                   10, MUTED).pack(anchor='w', pady=(2, 0))
        self.count_label = self.label(header, '', 12, WHITE, True)
        self.count_label.place(relx=1, rely=.1, anchor='ne')

        workspace = self.card(self.content)
        workspace.pack(fill='x', padx=22, pady=(0, 10))
        self.label(workspace, 'PROCESS INFORMATION', 17, WHITE, True).pack(anchor='w', padx=15, pady=(11, 7))
        inputs = ctk.CTkFrame(workspace, fg_color='transparent')
        inputs.pack(fill='x', padx=15)
        self.entries = []
        for i, (title, default) in enumerate([('Process ID', 'P5'), ('Arrival Time', '0'), ('Burst Time', '5')]):
            cell = ctk.CTkFrame(inputs, fg_color='transparent')
            cell.grid(row=0, column=i, padx=(0, 8) if i < 2 else 0, sticky='ew')
            inputs.grid_columnconfigure(i, weight=1)
            self.label(cell, title, 14, MUTED).pack(anchor='w')
            entry = ctk.CTkEntry(cell, height=33, corner_radius=4, fg_color=BLACK,
                                 border_color=BORDER, text_color=WHITE,
                                 font=('Segoe UI', 15))
            entry.bind('<FocusIn>', lambda e, w=entry: w.configure(border_color=ORANGE))
            entry.bind('<FocusOut>', lambda e, w=entry: w.configure(border_color=BORDER))
            entry.pack(fill='x', pady=(3, 0)); entry.insert(0, default)
            self.entries.append(entry)
        actions = ctk.CTkFrame(workspace, fg_color='transparent')
        actions.pack(fill='x', padx=15, pady=10)
        for text, fn, primary in [('+ Add Process', self.add_process, True),
                                  ('Remove Selected', self.remove_selected, False),
                                  ('Load Sample', self.load_sample, False),
                                  ('Clear All', self.clear_all, False)]:
            self.button(actions, text, fn, primary, 125).pack(side='left', padx=(0, 8))
        self.process_table = self.table(workspace, ('PID', 'Arrival Time', 'Burst Time'), 150)
        self.process_table.pack(fill='x', padx=15, pady=(0, 12))

        results = self.card(self.content)
        results.pack(fill='both', expand=True, padx=22, pady=(0, 18))
        bar = ctk.CTkFrame(results, fg_color='transparent')
        bar.pack(fill='x', padx=15, pady=(12, 5))
        self.tabs = {}
        for alg in ALGORITHMS + ['★ Comparison']:
            b = self.button(bar, alg, lambda a=alg: self.select_tab(a), False, 108)
            b.pack(side='left', padx=(0, 6)); self.tabs[alg] = b
        self.button(bar, 'Run All Algorithms', self.run_all, True, 170).pack(side='right')
        qbar = ctk.CTkFrame(results, fg_color='transparent')
        qbar.pack(fill='x', padx=15)
        self.label(qbar, 'Time Quantum (RR):', 12, MUTED).pack(side='left')
        self.quantum = ctk.CTkEntry(qbar, width=55, height=29, corner_radius=4,
                                    fg_color=BLACK, border_color=BORDER, font=('Segoe UI', 15))
        self.quantum.bind('<FocusIn>', lambda e: self.quantum.configure(border_color=ORANGE))
        self.quantum.bind('<FocusOut>', lambda e: self.quantum.configure(border_color=BORDER))
        self.quantum.pack(side='left', padx=8); self.quantum.insert(0, '3')
        self.heading = self.label(results, '', 19, WHITE, True)
        self.heading.pack(anchor='w', padx=15, pady=(9, 4))
        self.label(results, 'EXECUTION TIMELINE / GANTT CHART', 14, MUTED, True).pack(anchor='w', padx=15)
        chart_frame = ctk.CTkFrame(results, fg_color=BLACK, corner_radius=4, height=102)
        chart_frame.pack(fill='x', padx=15, pady=(5, 10))
        chart_frame.pack_propagate(False)
        self.chart = tk.Canvas(chart_frame, bg=BLACK, highlightthickness=0, height=95)
        self.chart.pack(fill='both', expand=True, padx=9, pady=5)
        self.chart.bind('<Configure>', lambda event: self.draw_chart())
        self.label(results, 'PROCESS DETAILS', 14, MUTED, True).pack(anchor='w', padx=15)
        self.metrics = self.table(results, ('PID', 'AT', 'BT', 'CT', 'TAT', 'WT', 'RT'), 175)
        self.metrics.pack(fill='x', padx=15, pady=(5, 8))
        self.metric_frame = ctk.CTkFrame(results, fg_color='transparent')
        self.metric_frame.pack(fill='x', padx=15, pady=(2, 9))
        self.metric_values = []
        for i, name in enumerate(('Average Turnaround', 'Average Waiting', 'Average Response')):
            tile = ctk.CTkFrame(self.metric_frame, fg_color=GRAY, corner_radius=4,
                                border_width=1, border_color='#704024')
            tile.grid(row=0, column=i, sticky='ew', padx=(0, 8) if i < 2 else 0)
            self.metric_frame.grid_columnconfigure(i, weight=1)
            self.label(tile, name, 14, MUTED).pack(pady=(8, 0))
            val = self.label(tile, '—', 26, ORANGE_LIGHT, True)
            val.pack(pady=(0, 8)); self.metric_values.append(val)
        self.status_box = ctk.CTkFrame(results, fg_color='#153A2A', corner_radius=4,
                                        border_width=1, border_color=ORANGE, height=39)
        self.status_box.pack(fill='x', padx=15, pady=(0, 12))
        self.status = self.label(self.status_box, 'Ready to simulate', 14, '#9AE6B4', True)
        self.status.pack(pady=9)
        # Separate comparison dashboard; the single-algorithm widgets are hidden in this mode.
        self.normal_widgets = list(results.winfo_children())[3:]  # chart heading through completion banner
        self.normal_pack = {w: w.pack_info() for w in self.normal_widgets}
        self.compare_frame = ctk.CTkFrame(results, fg_color='transparent')
    def build_comparison(self):
        for child in self.compare_frame.winfo_children():
            child.destroy()
        root = self.compare_frame
        if len(self.results) != len(ALGORITHMS):
            self.label(root, 'Run All Algorithms to generate the comparison dashboard.',
                       16, MUTED).pack(anchor='w', pady=25)
            return
        data = {name: self.results[name][2] for name in ALGORITHMS}
        best = [min(v[i] for v in data.values()) for i in range(3)]
        self.label(root, 'MULTI-ALGORITHM DASHBOARD', 15, MUTED, True).pack(
            anchor='w', pady=(4, 6))
        self.label(root, 'Lower average times indicate better performance. Green highlights the lowest value.',
                   14, MUTED).pack(anchor='w', pady=(0, 12))

        grid = ctk.CTkFrame(root, fg_color=GRAY, corner_radius=4)
        grid.pack(fill='x', pady=(0, 15))
        for i in range(4):
            grid.grid_columnconfigure(i, weight=1, uniform='compare')
        for col, title in enumerate(('Algorithm', 'Avg TAT', 'Avg WT', 'Avg RT')):
            self.label(grid, title, 16, '#161616', True, fg_color=ORANGE_LIGHT,
                       corner_radius=2).grid(row=0, column=col, pady=12, padx=5, sticky='ew')
        for r, name in enumerate(ALGORITHMS, 1):
            row_cells = []
            name_label = self.label(grid, name, 16, WHITE, True)
            name_label.grid(row=r, column=0, pady=10)
            row_cells.append(name_label)
            for i, value in enumerate(data[name]):
                winner = abs(value - best[i]) < 1e-9
                color = '#82E6B2' if winner else WHITE
                cell = self.label(grid, f'{value:.2f}' + ('  ★' if winner else ''),
                                  16, color, winner)
                cell.grid(row=r, column=i+1, pady=10)
                row_cells.append(cell)
            # All four cells react as one comparison row.
            for cell in row_cells:
                cell.bind('<Enter>', lambda e, cells=row_cells: [
                    w.configure(fg_color='#39302A') for w in cells])
                cell.bind('<Leave>', lambda e, cells=row_cells: [
                    w.configure(fg_color='transparent') for w in cells])

        cards = ctk.CTkFrame(root, fg_color='transparent')
        cards.pack(fill='x', pady=(0, 16))
        for i, title in enumerate(('Lowest Average Turnaround',
                                   'Lowest Average Waiting', 'Lowest Average Response')):
            cards.grid_columnconfigure(i, weight=1, uniform='cards')
            card = ctk.CTkFrame(cards, fg_color=GRAY, corner_radius=4,
                                border_width=1, border_color='#704024')
            card.grid(row=0, column=i, sticky='ew', padx=(0, 8) if i < 2 else 0)
            winners = [name for name in ALGORITHMS if abs(data[name][i]-best[i]) < 1e-9]
            self.label(card, title, 14, MUTED).pack(pady=(12, 2))
            self.label(card, f'{best[i]:.2f}', 26, ORANGE_LIGHT, True).pack()
            self.label(card, ', '.join(winners), 15, WHITE, True).pack(pady=(0, 12))

        self.label(root, 'AVERAGE WAITING TIME COMPARISON', 15, WHITE, True).pack(
            anchor='w', pady=(0, 8))
        maximum = max(data[name][1] for name in ALGORITHMS)
        for name in ALGORITHMS:
            line = ctk.CTkFrame(root, fg_color='transparent', height=33)
            line.pack(fill='x', pady=3)
            self.label(line, name, 15, WHITE, True, width=120, anchor='w').pack(side='left')
            self.label(line, f'{data[name][1]:.2f}', 15, WHITE, width=60).pack(side='right')
            track = ctk.CTkFrame(line, fg_color='#333333', height=18, corner_radius=2)
            track.pack(side='left', fill='x', expand=True, padx=12)
            track.pack_propagate(False)
            ratio = data[name][1] / maximum if maximum else 0
            if ratio:
                ctk.CTkFrame(track, fg_color='#82E6B2' if abs(data[name][1]-best[1]) < 1e-9
                             else ORANGE, corner_radius=2).place(
                                 relx=0, rely=0, relwidth=ratio, relheight=1)
        status = ctk.CTkFrame(root, fg_color='#153A2A', corner_radius=4,
                              border_width=1, border_color=ORANGE)
        status.pack(fill='x', pady=(18, 10))
        self.label(status, '✓ Simulation Completed!', 15, '#A7F3C4', True).pack(pady=12)
    def table(self, parent, columns, height):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Studio.Treeview', background=BLACK, fieldbackground=BLACK,
                        foreground=WHITE, rowheight=35, borderwidth=0, font=('Segoe UI', 15))
        style.configure('Studio.Treeview.Heading', background=ORANGE_LIGHT, foreground='#161616',
                        relief='flat', padding=(7, 9), font=('Segoe UI', 15, 'bold'))
        style.map('Studio.Treeview', background=[('selected', '#9C3300')],
                  foreground=[('selected', WHITE)])
        style.map('Studio.Treeview.Heading', background=[('active', ORANGE)],
                  foreground=[('active', WHITE)])
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=max(2, height // 35),
                            style='Studio.Treeview', selectmode='browse')
        tree.tag_configure('hover', background='#34271F', foreground=WHITE)
        tree._hover_row = None
        tree._hint_column = None
        tree.bind('<Motion>', lambda event, t=tree: self.table_hover(event, t))
        tree.bind('<Leave>', lambda event, t=tree: self.clear_table_hover(t))
        tree.bind('<ButtonPress-1>', lambda event: self.hide_tooltip())
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=90, minwidth=55, stretch=True)
        return tree
    def hide_tooltip(self):
        if self.tooltip is not None:
            try:
                self.tooltip.destroy()
            except tk.TclError:
                pass
            self.tooltip = None
    def table_hover(self, event, tree):
        region = tree.identify_region(event.x, event.y)
        row = tree.identify_row(event.y) if region == 'cell' else ''
        if row != tree._hover_row:
            if tree._hover_row and tree.exists(tree._hover_row):
                tree.item(tree._hover_row, tags=())
            tree._hover_row = row
            if row and row not in tree.selection():
                tree.item(row, tags=('hover',))
        col = tree.identify_column(event.x) if region == 'heading' else ''
        hint_key = (tree['columns'][int(col[1:]) - 1]
                    if col and col[1:].isdigit() else None)
        if hint_key != tree._hint_column:
            tree._hint_column = hint_key
            self.hide_tooltip()
            if hint_key in HINTS:
                tip = tk.Toplevel(self)
                tip.overrideredirect(True)
                tip.attributes('-topmost', True)
                tk.Label(tip, text=HINTS[hint_key], bg='#303030', fg=WHITE,
                         font=('Segoe UI', 12), padx=12, pady=7,
                         highlightbackground=ORANGE, highlightthickness=1).pack()
                tip.geometry(f'+{event.x_root + 14}+{event.y_root + 18}')
                self.tooltip = tip
    def clear_table_hover(self, tree):
        if tree._hover_row and tree.exists(tree._hover_row):
            tree.item(tree._hover_row, tags=())
        tree._hover_row = None
        tree._hint_column = None
        self.hide_tooltip()
    def refresh_processes(self):
        self.process_table.delete(*self.process_table.get_children())
        for p in self.processes:
            self.process_table.insert('', 'end', values=p)
        self.count_label.configure(text=f'{len(self.processes)} Processes')
    def invalidate(self):
        self.results.clear()
        self.refresh_processes()
        self.heading.configure(text='Run All Algorithms to update results')
        self.status.configure(text='● Process list changed — run simulation', text_color='#F5D08A')
        self.status_box.configure(fg_color='#40321E')
        self.select_tab(self.active)
    def add_process(self):
        try:
            pid = self.entries[0].get().strip()
            at = int(self.entries[1].get()); bt = int(self.entries[2].get())
            if not valid_process(pid, at, bt, self.processes):
                raise ValueError
            self.processes.append((pid, at, bt))
            self.entries[0].delete(0, 'end')
            self.entries[0].insert(0, f'P{len(self.processes) + 1}')
            self.invalidate()
        except ValueError:
            messagebox.showerror('Invalid input', 'Use a unique nonempty PID, arrival time ≥ 0, and burst time > 0.')
    def remove_selected(self):
        selected = self.process_table.selection()
        if not selected:
            messagebox.showinfo('Select process', 'Select a process in the table first.')
            return
        pid = self.process_table.item(selected[0], 'values')[0]
        self.processes = [p for p in self.processes if p[0] != pid]
        self.invalidate()
    def load_sample(self):
        self.processes = [('P1', 0, 6), ('P2', 1, 4), ('P3', 2, 2), ('P4', 3, 5)]
        self.invalidate()
    def clear_all(self):
        self.processes.clear(); self.invalidate()
    def run_all(self):
        if not self.processes:
            messagebox.showwarning('No processes', 'Add at least one process first.')
            return
        try:
            q = int(self.quantum.get())
            if q <= 0: raise ValueError
        except ValueError:
            messagebox.showerror('Invalid quantum', 'Round Robin time quantum must be a positive integer.')
            return
        self.results = {alg: schedule(self.processes, alg, q) for alg in ALGORITHMS}
        self.status.configure(text='✓ Simulation Completed!', text_color='#A7F3C4')
        self.status_box.configure(fg_color='#153A2A')
        self.select_tab(self.active)
    def select_tab(self, alg):
        self.active = alg
        for name, btn in self.tabs.items():
            btn.configure(fg_color=ORANGE if name == alg else GRAY,
                          hover_color=ORANGE_HOVER if name == alg else ORANGE,
                          border_width=1 if name == alg else 0,
                          border_color=ORANGE)
        if alg == '★ Comparison':
            self.heading.configure(text='Algorithm Performance Comparison')
            for widget in self.normal_widgets:
                widget.pack_forget()
            self.build_comparison()
            self.compare_frame.pack(fill='x', padx=15, pady=(4, 12))
        else:
            self.compare_frame.pack_forget()
            for widget in self.normal_widgets:
                # Restore original pack order and spacing saved before hiding.
                widget.pack(**self.normal_pack[widget])
            self.heading.configure(text=f'{alg} Scheduling Results')
            self.metrics.delete(*self.metrics.get_children())
            if alg in self.results:
                _, rows, averages = self.results[alg]
                for row in rows:
                    self.metrics.insert('', 'end', values=row)
                for value, avg in zip(self.metric_values, averages):
                    value.configure(text=f'{avg:.2f}')
            else:
                for value in self.metric_values:
                    value.configure(text='—')
            self.after(30, self.draw_chart)
    def draw_chart(self):
        c = self.chart; c.delete('all')
        if self.active not in self.results:
            c.create_text(12, 40, text='Run All Algorithms to generate the timeline',
                          anchor='w', fill=MUTED, font=('Segoe UI', 12))
            return
        segments = self.results[self.active][0]
        if not segments: return
        width = max(c.winfo_width(), 400)
        left, right, top, bottom = 22, width - 24, 16, 56
        total = segments[-1][2]
        scale = (right - left) / total
        palette = {p[0]: COLORS[i % len(COLORS)] for i, p in enumerate(self.processes)}
        for pid, start, end in segments:
            x1, x2 = left + start * scale, left + end * scale
            color = palette.get(pid, '#555555')
            c.create_rectangle(x1, top, x2, bottom, fill=color, outline=BLACK, width=1)
            if x2 - x1 > 20:
                c.create_text((x1+x2)/2, (top+bottom)/2, text=pid,
                              fill=WHITE, font=('Segoe UI', 18, 'bold'))
            c.create_line(x1, bottom, x1, bottom+5, fill=MUTED)
            c.create_text(x1, bottom+15, text=str(start), fill=MUTED,
                          font=('Segoe UI', 13, 'bold'))
        c.create_line(right, bottom, right, bottom+5, fill=MUTED)
        c.create_text(right, bottom+15, text=str(total), fill=MUTED,
                      font=('Segoe UI', 13, 'bold'))
