import customtkinter as ctk
import sqlite3

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Todo List Dashboard")
        self.geometry("1100x850") # Taller to fit the new Bar Graph nicely
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Main Layout (Grid Split) ---
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: TASK LIST 
        # ==========================================
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self.left_frame, text="My Tasks", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(0, 10), anchor="w")

        self.input_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        self.input_frame.pack(pady=10, fill="x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Task...", width=150)
        self.task_entry.pack(side="left", padx=(0, 10))

        self.desc_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Details...", width=200)
        self.desc_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_menu = ctk.CTkOptionMenu(
            self.input_frame, values=["High", "Medium", "Low"], variable=self.priority_var, width=100
        )
        self.priority_menu.pack(side="left", padx=(0, 10))

        self.add_button = ctk.CTkButton(self.input_frame, text="Add", width=80, command=self.add_task)
        self.add_button.pack(side="right")

        self.header_frame = ctk.CTkFrame(self.left_frame, fg_color="#2b2b2b", corner_radius=5)
        self.header_frame.pack(pady=(15, 0), fill="x")
        
        ctk.CTkLabel(self.header_frame, text="Task", width=150, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(self.header_frame, text="Priority", width=70, anchor="center", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(self.header_frame, text="Details", anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", fill="x", expand=True, padx=10, pady=5)
        ctk.CTkLabel(self.header_frame, text="Action", width=40, anchor="center", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10, pady=5)

        self.task_list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.task_list_frame.pack(pady=(5, 0), fill="both", expand=True)

        # ==========================================
        # RIGHT PANEL: KPI DASHBOARD
        # ==========================================
        self.right_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=10)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        # --- Progress Section ---
        ctk.CTkLabel(self.right_frame, text="Total Progress", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 0))
        self.pct_label = ctk.CTkLabel(self.right_frame, text="0%", font=ctk.CTkFont(size=42, weight="bold"), text_color="#1f6aa5")
        self.pct_label.pack(pady=(5, 0))
        self.progress_bar = ctk.CTkProgressBar(self.right_frame, width=220, height=12, corner_radius=10)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(5, 20))

        # --- Task Status Section ---
        ctk.CTkLabel(self.right_frame, text="Task Status", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5, 5))
        self.status_row = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.status_row.pack(fill="x", padx=15)

        self.comp_card = ctk.CTkFrame(self.status_row, fg_color="#3a3a3a", corner_radius=8)
        self.comp_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.comp_num = ctk.CTkLabel(self.comp_card, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#4dff4d")
        self.comp_num.pack(pady=(10, 0))
        ctk.CTkLabel(self.comp_card, text="Completed", font=ctk.CTkFont(size=12)).pack(pady=(0, 10))

        self.pend_card = ctk.CTkFrame(self.status_row, fg_color="#3a3a3a", corner_radius=8)
        self.pend_card.pack(side="left", fill="both", expand=True, padx=(5, 0))
        self.pend_num = ctk.CTkLabel(self.pend_card, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#ffa64d")
        self.pend_num.pack(pady=(10, 0))
        ctk.CTkLabel(self.pend_card, text="Pending", font=ctk.CTkFont(size=12)).pack(pady=(0, 10))

        # --- Priority Progress Section ---
        ctk.CTkLabel(self.right_frame, text="Priority Progress", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))
        self.prio_row = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.prio_row.pack(fill="x", padx=15)

        self.high_card = ctk.CTkFrame(self.prio_row, fg_color="#3a3a3a", corner_radius=8)
        self.high_card.pack(side="left", fill="both", expand=True, padx=(0, 3))
        ctk.CTkLabel(self.high_card, text="High", font=ctk.CTkFont(size=13, weight="bold"), text_color="#ff4d4d").pack(pady=(8, 2))
        self.high_pb = ctk.CTkProgressBar(self.high_card, height=6, progress_color="#ff4d4d", fg_color="#555555")
        self.high_pb.pack(fill="x", padx=10, pady=5)
        self.high_stats = ctk.CTkLabel(self.high_card, text="P: 0 | C: 0", font=ctk.CTkFont(size=11))
        self.high_stats.pack(pady=(0, 8))

        self.med_card = ctk.CTkFrame(self.prio_row, fg_color="#3a3a3a", corner_radius=8)
        self.med_card.pack(side="left", fill="both", expand=True, padx=(3, 3))
        ctk.CTkLabel(self.med_card, text="Medium", font=ctk.CTkFont(size=13, weight="bold"), text_color="#ffa64d").pack(pady=(8, 2))
        self.med_pb = ctk.CTkProgressBar(self.med_card, height=6, progress_color="#ffa64d", fg_color="#555555")
        self.med_pb.pack(fill="x", padx=10, pady=5)
        self.med_stats = ctk.CTkLabel(self.med_card, text="P: 0 | C: 0", font=ctk.CTkFont(size=11))
        self.med_stats.pack(pady=(0, 8))

        self.low_card = ctk.CTkFrame(self.prio_row, fg_color="#3a3a3a", corner_radius=8)
        self.low_card.pack(side="left", fill="both", expand=True, padx=(3, 0))
        ctk.CTkLabel(self.low_card, text="Low", font=ctk.CTkFont(size=13, weight="bold"), text_color="#4dff4d").pack(pady=(8, 2))
        self.low_pb = ctk.CTkProgressBar(self.low_card, height=6, progress_color="#4dff4d", fg_color="#555555")
        self.low_pb.pack(fill="x", padx=10, pady=5)
        self.low_stats = ctk.CTkLabel(self.low_card, text="P: 0 | C: 0", font=ctk.CTkFont(size=11))
        self.low_stats.pack(pady=(0, 8))

        # ==========================================
        # NEW VISUAL: THE BAR GRAPH
        # ==========================================
        self.graph_card = ctk.CTkFrame(self.right_frame, fg_color="#3a3a3a", corner_radius=8)
        self.graph_card.pack(fill="both", expand=True, padx=15, pady=(15, 20))

        # 1. Legend at the top
        self.legend_frame = ctk.CTkFrame(self.graph_card, fg_color="transparent")
        self.legend_frame.pack(pady=(10, 0))

        ctk.CTkFrame(self.legend_frame, width=12, height=12, fg_color="#0f0aa4", corner_radius=2).pack(side="left", padx=5)
        ctk.CTkLabel(self.legend_frame, text="Pending", font=ctk.CTkFont(size=11)).pack(side="left", padx=(0, 15))

        ctk.CTkFrame(self.legend_frame, width=12, height=12, fg_color="#27a2ff", corner_radius=2).pack(side="left", padx=5)
        ctk.CTkLabel(self.legend_frame, text="Completed", font=ctk.CTkFont(size=11)).pack(side="left")

        # 2. Graph Area
        self.bar_area = ctk.CTkFrame(self.graph_card, fg_color="transparent")
        self.bar_area.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # 3. Base Axis Line
        self.axis_line = ctk.CTkFrame(self.bar_area, height=2, fg_color="#666666")
        self.axis_line.place(relx=0.5, rely=0.85, relwidth=0.9, anchor="center")

        # 4. X-Axis Labels (Fixed at the bottom)
        ctk.CTkLabel(self.bar_area, text="High", font=ctk.CTkFont(size=11, weight="bold"), text_color="#ff4d4d").place(relx=0.20, rely=0.98, anchor="s")
        ctk.CTkLabel(self.bar_area, text="Medium", font=ctk.CTkFont(size=11, weight="bold"), text_color="#ffa64d").place(relx=0.50, rely=0.98, anchor="s")
        ctk.CTkLabel(self.bar_area, text="Low", font=ctk.CTkFont(size=11, weight="bold"), text_color="#4dff4d").place(relx=0.80, rely=0.98, anchor="s")

        # 5. Define Bar Shapes (Height mapped dynamically in update_dashboard)
        self.bar_hp = ctk.CTkFrame(self.bar_area, fg_color="#0f0aa4", corner_radius=3)
        self.bar_hc = ctk.CTkFrame(self.bar_area, fg_color="#27a2ff", corner_radius=3)
        self.bar_mp = ctk.CTkFrame(self.bar_area, fg_color="#0f0aa4", corner_radius=3)
        self.bar_mc = ctk.CTkFrame(self.bar_area, fg_color="#27a2ff", corner_radius=3)
        self.bar_lp = ctk.CTkFrame(self.bar_area, fg_color="#0f0aa4", corner_radius=3)
        self.bar_lc = ctk.CTkFrame(self.bar_area, fg_color="#27a2ff", corner_radius=3)

        # 6. Define Floating Numbers above bars
        self.lbl_hp = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))
        self.lbl_hc = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))
        self.lbl_mp = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))
        self.lbl_mc = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))
        self.lbl_lp = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))
        self.lbl_lc = ctk.CTkLabel(self.bar_area, text="0", font=ctk.CTkFont(size=11))

        # --- Database Setup & Initial Load ---
        self.conn = sqlite3.connect("task.db")
        self.create_table()
        self.load_tasks()

    # --- Database Methods ---
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'Medium',
                is_completed INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def add_task(self):
        task_text = self.task_entry.get()
        desc_text = self.desc_entry.get()
        priority_val = self.priority_var.get()
        
        if task_text.strip() == "": return 
            
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name, description, priority) VALUES (?, ?, ?)", 
            (task_text, desc_text, priority_val))
        self.conn.commit()
        
        self.task_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.priority_var.set("Medium") 
        self.load_tasks()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def toggle_task(self, task_id, current_state):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET is_completed = ? WHERE id = ?", (current_state, task_id))
        self.conn.commit()
        self.load_tasks()

    def load_tasks(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, task_name, description, priority, is_completed FROM tasks")
        tasks = cursor.fetchall()

        total_tasks = len(tasks)
        completed_tasks = 0
        hp, hc = 0, 0
        mp, mc = 0, 0
        lp, lc = 0, 0

        for task_id, task_name, description, priority, is_completed in tasks:
            if is_completed:
                completed_tasks += 1
                if priority == "High": hc += 1
                elif priority == "Medium": mc += 1
                elif priority == "Low": lc += 1
            else:
                if priority == "High": hp += 1
                elif priority == "Medium": mp += 1
                elif priority == "Low": lp += 1

            row_frame = ctk.CTkFrame(self.task_list_frame, fg_color="#333333", corner_radius=5)
            row_frame.pack(fill="x", pady=3)

            check_var = ctk.IntVar(value=is_completed)
            
            task_checkbox = ctk.CTkCheckBox(row_frame, text=task_name, variable=check_var, width=150,
                font=ctk.CTkFont(size=14, overstrike=(is_completed == 1)),
                command=lambda t_id=task_id, var=check_var: self.toggle_task(t_id, var.get()))
            task_checkbox.pack(side="left", padx=10, pady=8)

            color_map = {"High": "#ff4d4d", "Medium": "#ffa64d", "Low": "#4dff4d"}
            prio_color = color_map.get(priority, "white")
            
            prio_label = ctk.CTkLabel(row_frame, text=priority, width=70, text_color=prio_color,
                font=ctk.CTkFont(weight="bold", overstrike=(is_completed == 1)))
            prio_label.pack(side="left", padx=10)

            display_desc = description if description else "-"
            desc_label = ctk.CTkLabel(row_frame, text=display_desc, anchor="w",
                text_color="gray70" if is_completed else "white",
                font=ctk.CTkFont(size=13, overstrike=(is_completed == 1)))
            desc_label.pack(side="left", fill="x", expand=True, padx=10)

            delete_btn = ctk.CTkButton(row_frame, text="X", width=40, fg_color="#cc0000",
                hover_color="#990000", command=lambda t_id=task_id: self.delete_task(t_id))
            delete_btn.pack(side="right", padx=10)

        self.update_dashboard(total_tasks, completed_tasks, hp, hc, mp, mc, lp, lc)

    # --- Graphing Engine Helper ---
    def _draw_single_bar(self, bar_widget, label_widget, val, max_val, max_relheight, center_x):
        """Calculates exact height and maps the bar to the graph UI."""
        if val == 0:
            bar_widget.place_forget()  # Hide if zero
            label_widget.place_forget()
        else:
            # Calculate height proportional to the maximum value on the board
            bar_height = (val / max_val) * max_relheight
            
            # Draw the bar growing up from the bottom line
            bar_widget.place(relx=center_x, rely=0.85, relwidth=0.06, relheight=bar_height, anchor="s")
            
            # Place the number label just above the top of the bar
            label_widget.place(relx=center_x, rely=0.85 - bar_height - 0.01, anchor="s")
            label_widget.configure(text=str(val))

    def update_dashboard(self, total, completed, hp, hc, mp, mc, lp, lc):
        """Updates all cards, progress bars, and the Bar Chart."""
        pending = total - completed
        pct = (completed / total * 100) if total > 0 else 0
        
        self.pct_label.configure(text=f"{int(pct)}%")
        self.progress_bar.set(pct / 100.0)

        self.comp_num.configure(text=str(completed))
        self.pend_num.configure(text=str(pending))
        
        h_tot, m_tot, l_tot = hp + hc, mp + mc, lp + lc
        self.high_pb.set(hc / h_tot if h_tot > 0 else 0)
        self.high_stats.configure(text=f"P: {hp} | C: {hc}")
        self.med_pb.set(mc / m_tot if m_tot > 0 else 0)
        self.med_stats.configure(text=f"P: {mp} | C: {mc}")
        self.low_pb.set(lc / l_tot if l_tot > 0 else 0)
        self.low_stats.configure(text=f"P: {lp} | C: {lc}")

        # === BAR GRAPH UPDATE MATH ===
        # Find the tallest bar so we can scale everything else properly
        max_v = max(hp, hc, mp, mc, lp, lc)
        if max_v == 0: max_v = 1 # Prevent division by zero if board is empty
        
        # Max bar height will consume 65% of the graph area so numbers don't get cut off
        m_rh = 0.65 

        # High group centers around 0.20
        self._draw_single_bar(self.bar_hp, self.lbl_hp, hp, max_v, m_rh, center_x=0.16)
        self._draw_single_bar(self.bar_hc, self.lbl_hc, hc, max_v, m_rh, center_x=0.24)

        # Medium group centers around 0.50
        self._draw_single_bar(self.bar_mp, self.lbl_mp, mp, max_v, m_rh, center_x=0.46)
        self._draw_single_bar(self.bar_mc, self.lbl_mc, mc, max_v, m_rh, center_x=0.54)

        # Low group centers around 0.80
        self._draw_single_bar(self.bar_lp, self.lbl_lp, lp, max_v, m_rh, center_x=0.76)
        self._draw_single_bar(self.bar_lc, self.lbl_lc, lc, max_v, m_rh, center_x=0.84)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()