import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from plyer import notification

class DesktopNotifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Desktop Notifier")
        self.root.geometry("620x680")
        self.root.resizable(False, False)

        # Track active recurring loop threads
        self.recurring_active = False

        # Apply basic styling / theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.setup_ui()

    def setup_ui(self):
        # --- TITLE ---
        header = ttk.Label(
            self.root, 
            text="🔔 Desktop Notification Manager", 
            font=("Segoe UI", 16, "bold")
        )
        header.pack(pady=10)

        # --- NOTEBOOK (TABS) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=5)

        self.tab_send = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_send, text=" Create & Schedule ")
        self.notebook.add(self.tab_history, text=" Notification History ")

        # Build Tabs Content
        self.build_send_tab()
        self.build_history_tab()

    def build_send_tab(self):
        # Quick Presets Frame
        preset_frame = ttk.LabelFrame(self.tab_send, text=" Quick Presets ")
        preset_frame.pack(fill="x", padx=10, pady=5)

        self.preset_var = tk.StringVar(value="Select Preset...")
        presets = [
            "Hydration Break",
            "Posture Check",
            "Eye Rest (20-20-20 Rule)",
            "Meeting Reminder"
        ]
        preset_cb = ttk.Combobox(preset_frame, textvariable=self.preset_var, values=presets, state="readonly")
        preset_cb.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        preset_cb.bind("<<ComboboxSelected>>", self.apply_preset)

        # Form Controls Frame
        form_frame = ttk.LabelFrame(self.tab_send, text=" Notification Details ")
        form_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Title
        ttk.Label(form_frame, text="Notification Title:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_title = ttk.Entry(form_frame, width=45)
        self.entry_title.grid(row=0, column=1, columnspan=2, sticky="w", padx=10, pady=5)
        self.entry_title.insert(0, "Python Alert")

        # Message Body
        ttk.Label(form_frame, text="Message Body:").grid(row=1, column=0, sticky="nw", padx=10, pady=5)
        self.txt_message = tk.Text(form_frame, width=34, height=4, font=("Segoe UI", 9))
        self.txt_message.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=5)
        self.txt_message.insert("1.0", "This is your custom desktop notification!")

        # Custom Icon (.ico on Windows)
        ttk.Label(form_frame, text="Custom Icon (.ico):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_icon = ttk.Entry(form_frame, width=32)
        self.entry_icon.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        btn_browse = ttk.Button(form_frame, text="Browse", command=self.browse_icon)
        btn_browse.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Display Timeout (Seconds)
        ttk.Label(form_frame, text="Display Timeout (s):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.spin_timeout = ttk.Spinbox(form_frame, from_=1, to=60, width=10)
        self.spin_timeout.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.spin_timeout.set(10)

        # Delay Before Trigger (Seconds/Minutes)
        ttk.Label(form_frame, text="Delay (Seconds):").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.spin_delay = ttk.Spinbox(form_frame, from_=0, to=3600, width=10)
        self.spin_delay.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.spin_delay.set(0)

        # Options: Sound & Repeat Loop
        self.chk_sound_var = tk.BooleanVar(value=True)
        self.chk_sound = ttk.Checkbutton(form_frame, text="Play System Sound Alert", variable=self.chk_sound_var)
        self.chk_sound.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.chk_repeat_var = tk.BooleanVar(value=False)
        self.chk_repeat = ttk.Checkbutton(form_frame, text="Repeat Every 'Delay' Interval", variable=self.chk_repeat_var)
        self.chk_repeat.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(self.tab_send)
        btn_frame.pack(fill="x", padx=10, pady=10)

        btn_send = ttk.Button(btn_frame, text="🚀 Send / Start Notification", command=self.start_notification)
        btn_send.pack(side="left", padx=5, expand=True, fill="x")

        btn_stop = ttk.Button(btn_frame, text="⏹ Stop Recurring Loop", command=self.stop_recurring)
        btn_stop.pack(side="right", padx=5, expand=True, fill="x")

    def build_history_tab(self):
        # History Table (Treeview)
        columns = ("Time", "Title", "Message")
        self.history_tree = ttk.Treeview(self.tab_history, columns=columns, show="headings", height=15)
        
        self.history_tree.heading("Time", text="Timestamp")
        self.history_tree.heading("Title", text="Title")
        self.history_tree.heading("Message", text="Message Content")

        self.history_tree.column("Time", width=120)
        self.history_tree.column("Title", width=150)
        self.history_tree.column("Message", width=280)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.tab_history, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

    # --- ACTION HANDLERS ---
    def browse_icon(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")]
        )
        if filepath:
            self.entry_icon.delete(0, tk.END)
            self.entry_icon.insert(0, filepath)

    def apply_preset(self, event=None):
        selection = self.preset_var.get()
        self.txt_message.delete("1.0", tk.END)
        self.entry_title.delete(0, tk.END)

        if selection == "Hydration Break":
            self.entry_title.insert(0, "💧 Drink Water")
            self.txt_message.insert("1.0", "Time to drink a glass of water and stay hydrated!")
        elif selection == "Posture Check":
            self.entry_title.insert(0, "🪑 Posture Check")
            self.txt_message.insert("1.0", "Sit up straight, roll your shoulders back, and relax your neck.")
        elif selection == "Eye Rest (20-20-20 Rule)":
            self.entry_title.insert(0, "👀 Eye Strain Prevention")
            self.txt_message.insert("1.0", "Look away from the screen at an object 20 feet away for 20 seconds.")
        elif selection == "Meeting Reminder":
            self.entry_title.insert(0, "📅 Upcoming Meeting")
            self.txt_message.insert("1.0", "Your scheduled meeting is starting soon. Prepare your notes.")

    def log_history(self, title, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.history_tree.insert("", 0, values=(now, title, msg))

    def trigger_sound(self):
        if self.chk_sound_var.get():
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                # Standard bell chime fallback across platforms
                self.root.bell()

    def send_desktop_notification(self, title, message, timeout, icon_path):
        kwargs = {
            "title": title,
            "message": message,
            "timeout": int(timeout)
        }
        if icon_path and os.path.exists(icon_path):
            kwargs["app_icon"] = icon_path

        # Play sound alert
        self.trigger_sound()

        # Fire desktop popup
        notification.notify(**kwargs)

        # Update History Log on GUI thread safely
        self.root.after(0, self.log_history, title, message)

    def notification_worker(self, title, message, timeout, delay, is_recurring, icon_path):
        while True:
            if delay > 0:
                time.sleep(delay)

            self.send_desktop_notification(title, message, timeout, icon_path)

            # If repeat loop is checked, keep cycling; otherwise break
            if not is_recurring or not self.recurring_active:
                break

    def start_notification(self):
        title = self.entry_title.get().strip()
        message = self.txt_message.get("1.0", tk.END).strip()
        icon_path = self.entry_icon.get().strip()

        try:
            timeout = int(self.spin_timeout.get())
            delay = int(self.spin_delay.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Timeout and Delay must be integer numbers.")
            return

        if not title or not message:
            messagebox.showwarning("Empty Fields", "Title and Message fields cannot be empty.")
            return

        is_recurring = self.chk_repeat_var.get()
        if is_recurring and delay <= 0:
            messagebox.showwarning("Loop Error", "Please specify a delay greater than 0 seconds for recurring notifications.")
            return

        self.recurring_active = True

        # Run in a separate thread so GUI remains responsive
        threading.Thread(
            target=self.notification_worker,
            args=(title, message, timeout, delay, is_recurring, icon_path),
            daemon=True
        ).start()

        if delay > 0:
            messagebox.showinfo("Scheduled", f"Notification scheduled to trigger in {delay} seconds.")
        else:
            messagebox.showinfo("Success", "Notification sent successfully!")

    def stop_recurring(self):
        if self.recurring_active:
            self.recurring_active = False
            messagebox.showinfo("Stopped", "Recurring notification loop has been disabled.")
        else:
            messagebox.showinfo("Info", "No recurring notification is currently active.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopNotifierApp(root)
    root.mainloop()