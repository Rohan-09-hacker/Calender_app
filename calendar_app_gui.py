import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import threading
import calendar_engine

# Set the global theme to dark appearance mode
ctk.set_appearance_mode("dark")

class PremiumCalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Pinnacle Time Manager PRO")
        self.geometry("900x650")
        self.configure(fg_color="#0f1115")  # Ultra-dark charcoal backdrop (New Base)
        self.resizable(False, False)

        # Initialize SQLite storage layer matrix
        calendar_engine.init_db()

        # --- Main Layout Split Panel ---
        self.grid_columnconfigure(0, weight=4, minsize=420)
        self.grid_columnconfigure(1, weight=5, minsize=480)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # LEFT PANEL: Calendar & Header Banner
        # ==========================================
        # Changed to a deep slate blue-gray contrast panel
        self.left_panel = ctk.CTkFrame(self, fg_color="#171a21", corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(
            self.left_panel, 
            text="📅   TIME MANAGER PRO", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#00b4d8"  # Electric cyan header accent
        )
        self.logo_label.pack(pady=(35, 20))

        # Visual Wrapper Card
        self.cal_card = ctk.CTkFrame(self.left_panel, fg_color="#1f242e", corner_radius=16)
        self.cal_card.pack(pady=10, padx=25, fill="x")

        self.cal = Calendar(
            self.cal_card, 
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            font=("Segoe UI", 11),
            background='#1f242e',          # New inner slate background
            foreground='#e2e8f0',          # Soft white font
            headersbackground='#2d3748',   # Strong gray header block
            headersforeground='#e2e8f0',
            selectbackground='#00b4d8',    # Electric cyan active day highlight
            selectforeground='#0f1115',
            normalbackground='#1f242e',
            normalforeground='#e2e8f0',
            weekendbackground='#171a21',
            weekendforeground='#ff6b6b',   # Bright pastel red for weekends
            othermonthbackground='#13161c',
            othermonthforeground='#4a5568',
            bd=0
        )
        self.cal.pack(pady=15, padx=15, fill="x")
        self.cal.bind("<<CalendarSelected>>", lambda event: self.trigger_async_refresh())

        # Subtle Status Footer Banner
        self.status_footer = ctk.CTkLabel(
            self.left_panel,
            text="⚡ Database Engine Connected: Local SQLite Matrix",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"),
            text_color="#4a5568"
        )
        self.status_footer.pack(side="bottom", pady=20)

        # ==========================================
        # RIGHT PANEL: Smooth Inputs & List Views
        # ==========================================
        self.right_panel = ctk.CTkFrame(self, fg_color="#0f1115", corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=0)

        # --- Dynamic Header ---
        self.task_header = ctk.CTkLabel(
            self.right_panel, 
            text="📊   YOUR SCHEDULED WORKSPACE", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#e2e8f0"
        )
        self.task_header.pack(anchor="w", pady=(35, 15))

        # --- Task Logging Window Panel ---
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.right_panel, 
            fg_color="#171a21",          # Deep slate inner frame
            corner_radius=12,
            border_width=1,
            border_color="#2d3748"       # Sharp gray border bounds
        )
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 20))

        # --- Input Action Deck Card ---
        self.action_card = ctk.CTkFrame(self.right_panel, fg_color="#171a21", corner_radius=16, border_width=1, border_color="#2d3748")
        self.action_card.pack(fill="x", pady=(0, 35), ipady=10)

        self.input_title = ctk.CTkLabel(self.action_card, text="＋ CREATE NEW EVENT", font=ctk.CTkFont(size=12, weight="bold"), text_color="#2ecc71") # Crisp mint emerald
        self.input_title.pack(anchor="w", padx=20, pady=(15, 8))

        self.form_row = ctk.CTkFrame(self.action_card, fg_color="transparent")
        self.form_row.pack(fill="x", padx=15)

        # Animated Hover Entry Field for Time
        self.time_entry = ctk.CTkEntry(
            self.form_row, 
            placeholder_text="12:00", 
            width=80,
            font=("Segoe UI", 12),
            height=38,
            fg_color="#252b36",
            border_color="#4a5568",
            placeholder_text_color="#4a5568",
            text_color="#e2e8f0"
        )
        self.time_entry.pack(side="left", padx=5)
        self.time_entry.insert(0, "12:00")

        # Animated Hover Entry Field for Description
        self.desc_entry = ctk.CTkEntry(
            self.form_row, 
            placeholder_text="Enter task description here...", 
            font=("Segoe UI", 12),
            height=38,
            fg_color="#252b36",
            border_color="#4a5568",
            placeholder_text_color="#4a5568",
            text_color="#e2e8f0"
        )
        self.desc_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Smooth Interactive Add Button
        self.add_btn = ctk.CTkButton(
            self.form_row, 
            text="Save Entry", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#2ecc71",          # Solid Emerald green core
            hover_color="#27ae60",     # Deep dynamic tracking green
            text_color="#0f1115",
            width=100,
            height=38,
            corner_radius=8,
            command=self.save_new_reminder
        )
        self.add_btn.pack(side="right", padx=5)

        self.current_reminders = []
        self.trigger_async_refresh()

    def trigger_async_refresh(self):
        threading.Thread(target=self.refresh_reminder_list, daemon=True).start()

    def refresh_reminder_list(self):
        selected_date = self.cal.get_date()
        reminders = calendar_engine.get_reminders_for_date(selected_date)

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not reminders:
            empty_msg = ctk.CTkLabel(
                self.scrollable_frame, 
                text="✨   Workspace Cleared! No tasks for this day.", 
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal"),
                text_color="#4a5568"
            )
            empty_msg.pack(pady=40)
            return

        for item in reminders:
            rem_id, r_time, r_title = item
            
            # Individual task card block
            task_card = ctk.CTkFrame(self.scrollable_frame, fg_color="#1f242e", height=50, corner_radius=8)
            task_card.pack(fill="x", pady=5, padx=5)
            task_card.pack_propagate(False)

            # High-fidelity clock badge tag
            time_badge = ctk.CTkLabel(
                task_card, 
                text=f" ⏰ {r_time} ", 
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                fg_color="#2d3748",
                text_color="#00b4d8", # Electric cyan text
                corner_radius=6
            )
            time_badge.pack(side="left", padx=12, pady=10)

            # Task Description String Wrap
            title_text = ctk.CTkLabel(
                task_card, 
                text=r_title, 
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color="#e2e8f0"
            )
            title_text.pack(side="left", padx=5)

            # Individual modern sleek delete button
            item_del_btn = ctk.CTkButton(
                task_card,
                text="🗑️",
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color="#ff6b6b",  # Transitions to premium warning red on pointer hover
                text_color="#ff6b6b",
                width=35,
                height=30,
                corner_radius=6,
                command=lambda id_to_drop=rem_id: self.remove_reminder_by_id(id_to_drop)
            )
            item_del_btn.pack(side="right", padx=12)

    def save_new_reminder(self):
        selected_date = self.cal.get_date()
        target_time = self.time_entry.get().strip()
        task_title = self.desc_entry.get().strip()

        if not task_title:
            messagebox.showwarning("Form Incomplete", "Please describe your upcoming schedule item before saving.")
            return

        success = calendar_engine.add_reminder(selected_date, target_time, task_title)
        if success:
            self.desc_entry.delete(0, ctk.END)
            self.trigger_async_refresh()
        else:
            messagebox.showerror("Validation Failure", "Ensure targeted timestamp field maps to the format HH:MM precisely (e.g., 09:15).")

    def remove_reminder_by_id(self, db_id):
        calendar_engine.delete_reminder(db_id)
        self.trigger_async_refresh()

if __name__ == "__main__":
    app = PremiumCalendarApp()
    app.mainloop()