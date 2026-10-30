import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from plyer import notification

# --- THEME COLOR PALETTES ---
THEMES = {
    "Dark Glossy": {
        "bg": "#1e1e2e",
        "card_bg": "#181825",
        "fg": "#cdd6f4",
        "accent": "#89b4fa",
        "accent_fg": "#1e1e2e",
        "entry_bg": "#313244",
        "entry_fg": "#cdd6f4",
        "tree_bg": "#11111b",
        "tree_fg": "#cdd6f4"
    },
    "Light Modern": {
        "bg": "#f4f6f9",
        "card_bg": "#ffffff",
        "fg": "#2d3748",
        "accent": "#3182ce",
        "accent_fg": "#ffffff",
        "entry_bg": "#edf2f7",
        "entry_fg": "#2d3748",
        "tree_bg": "#ffffff",
        "tree_fg": "#2d3748"
    },
    "Cyberpunk Neon": {
        "bg": "#0f051d",
        "card_bg": "#1a0b2e",
        "fg": "#00ffcc",
        "accent": "#ff007f",
        "accent_fg": "#ffffff",
        "entry_bg": "#2b104a",
        "entry_fg": "#00ffcc",
        "tree_bg": "#090214",
        "tree_fg": "#00ffcc"
    }
}

class ModernDesktopNotifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Desktop Notifier")
        self.root.geometry("660x720")
        self.root.resizable(False, False)

        self.current_theme_name = "Dark Glossy"
        self.theme = THEMES[self.current_theme_name]
        self.recurring_active = False

        self.setup_styles()
        self.build_ui()
        self.apply_theme()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def apply_theme(self):
        t = self.theme
        # Configure root background
        self.root.configure(bg=t["bg"])

        # Update ttk styles dynamically
        self.style.configure(".", background=t["bg"], foreground=t["fg"], font=("Segoe UI", 10))
        self.style.configure("TLabel", background=t["bg"], foreground=t["fg"])
        self.style.configure("TNotebook", background=t["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=t["card_bg"], foreground=t["fg"], padding=[12, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", t["accent"])], foreground=[("selected", t["accent_fg"])])
        
        self.style.configure("TLabelframe", background=t["bg"], foreground=t["accent"], font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=t["bg"], foreground=t["accent"])
        
        self.style.configure("TButton", background=t["accent"], foreground=t["accent_fg"], font=("Segoe UI", 10, "bold"), borderwidth=0, focusthickness=3, focuscolor="none")
        self.style.map("TButton", background=[('active', t["fg"])])

        self.style.configure("TCheckbutton", background=t["bg"], foreground=t["fg"])
        
        # Treeview styling
        self.style.configure("Treeview", background=t["tree_bg"], foreground=t["tree_fg"], fieldbackground=t["tree_bg"], borderwidth=0)
        self.style.configure("Treeview.Heading", background=t["accent"], foreground=t["accent_fg"], font=("Segoe UI", 9, "bold"))

        # Re-color widgets that don't use ttk styles directly
        self.update_widget_colors(self.root)

    def update_widget_colors(self, widget):
        t = self.theme
        for child in widget.winfo_children():
            w_type = child.winfo_class()
            if w_type in ("Text", "Entry"):
                try:
                    child.configure(bg=t["entry_bg"], fg=t["entry_fg"], insertbackground=t["fg"])
                except Exception:
                    pass
            elif w_type == "Frame" or w_type == "Labelframe":
                try:
                    child.configure(bg=t["bg"])
                except Exception:
                    pass
            self.update_widget_colors(child)

    def change_theme(self, event=None):
        selected = self.theme_var.get()
        if selected in THEMES:
            self.current_theme_name = selected
            self.theme = THEMES[selected]
            self.apply_theme()

    def build_ui(self):
        # Top Header Bar with Theme Switcher
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=15)

        title_lbl = ttk.Label(header_frame, text="⚡ Glossy Desktop Notifier", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(side="left")

        theme_lbl = ttk.Label(header_frame, text="Theme:", font=("Segoe UI", 9))
        theme_lbl.pack(side="left", padx=(20, 5))

        self.theme_var = tk.StringVar(value=self.current_theme_name)
        theme_cb = ttk.Combobox(header_frame, textvariable=self.theme_var, values=list(THEMES.keys()), state="readonly", width=15)
        theme_cb.pack(side="left")
        theme_cb.bind("<<ComboboxSelected>>", self.change_theme)

        # Notebook Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=5)

        self.tab_send = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_send, text=" ✨ Create Notification ")
        self.notebook.add(self.tab_history, text=" 📜 History Log ")

        self.build_send_tab()
        self.build_history_tab()

    def build_send_tab(self):
        # Presets
        preset_frame = ttk.LabelFrame(self.tab_send, text=" Quick Presets ")
        preset_frame.pack(fill="x", padx=10, pady=8)

        self.preset_var = tk.StringVar(value="Choose a template...")
        presets = ["Hydration Break", "Posture Check", "Eye Rest (20-20-20)", "Meeting Reminder"]
        preset_cb = ttk.Combobox(preset_frame, textvariable=self.preset_var, values=presets, state="readonly")
        preset_cb.pack(side="left", padx=10, pady=8, fill="x", expand=True)
        preset_cb.bind("<<ComboboxSelected>>", self.apply_preset)

        # Form Controls
        form_frame = ttk.LabelFrame(self.tab_send, text=" Configuration ")
        form_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=12, pady=6)
        self.entry_title = ttk.Entry(form_frame, width=42, font=("Segoe UI", 10))
        self.entry_title.grid(row=0, column=1, columnspan=2, sticky="w", padx=10, pady=6)
        self.entry_title.insert(0, "Glossy Alert")

        ttk.Label(form_frame, text="Message:").grid(row=1, column=0, sticky="nw", padx=12, pady=6)
        self.txt_message = tk.Text(form_frame, width=32, height=4, font=("Segoe UI", 10), relief="flat", highlightthickness=1)
        self.txt_message.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=6)
        self.txt_message.insert("1.0", "Your custom desktop alert message goes here!")

        ttk.Label(form_frame, text="Custom Icon (.ico):").grid(row=2, column=0, sticky="w", padx=12, pady=6)
        self.entry_icon = ttk.Entry(form_frame, width=30, font=("Segoe UI", 10))
        self.entry_icon.grid(row=2, column=1, sticky="w", padx=10, pady=6)
        btn_browse = ttk.Button(form_frame, text="Browse", command=self.browse_icon)
        btn_browse.grid(row=2, column=2, sticky="w", padx=5, pady=6)

        ttk.Label(form_frame, text="Timeout (secs):").grid(row=3, column=0, sticky="w", padx=12, pady=6)
        self.spin_timeout = ttk.Spinbox(form_frame, from_=1, to=60, width=10)
        self.spin_timeout.grid(row=3, column=1, sticky="w", padx=10, pady=6)
        self.spin_timeout.set(8)

        ttk.Label(form_frame, text="Delay / Interval (s):").grid(row=4, column=0, sticky="w", padx=12, pady=6)
        self.spin_delay = ttk.Spinbox(form_frame, from_=0, to=3600, width=10)
        self.spin_delay.grid(row=4, column=1, sticky="w", padx=10, pady=6)
        self.spin_delay.set(0)

        self.chk_sound_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Play System Chime Audio", variable=self.chk_sound_var).grid(row=5, column=0, columnspan=2, sticky="w", padx=12, pady=6)

        self.chk_repeat_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(form_frame, text="Enable Recurring Loop (Repeats every Delay interval)", variable=self.chk_repeat_var).grid(row=6, column=0, columnspan=2, sticky="w", padx=12, pady=6)

        # Action Buttons
        btn_frame = ttk.Frame(self.tab_send)
        btn_frame.pack(fill="x", padx=10, pady=12)

        btn_send = ttk.Button(btn_frame, text="🚀 Send Notification Now", command=self.start_notification)
        btn_send.pack(side="left", padx=5, expand=True, fill="x", ipady=4)

        btn_stop = ttk.Button(btn_frame, text="⏹ Stop Loop", command=self.stop_recurring)
        btn_stop.pack(side="right", padx=5, expand=True, fill="x", ipady=4)

    def build_history_tab(self):
        columns = ("Time", "Title", "Message")
        self.history_tree = ttk.Treeview(self.tab_history, columns=columns, show="headings", height=16)
        
        self.history_tree.heading("Time", text="Timestamp")
        self.history_tree.heading("Title", text="Title")
        self.history_tree.heading("Message", text="Message Content")

        self.history_tree.column("Time", width=110, anchor="center")
        self.history_tree.column("Title", width=140)
        self.history_tree.column("Message", width=290)

        scrollbar = ttk.Scrollbar(self.tab_history, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

        # Export History Button below treeview
        btn_export = ttk.Button(self.tab_history, text="📥 Export History to File", command=self.export_history)
        btn_export.pack(side="bottom", fill="x", padx=10, pady=10, ipady=3)

    # --- FUNCTIONALITY HANDLERS ---
    def browse_icon(self):
        filepath = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")])
        if filepath:
            self.entry_icon.delete(0, tk.END)
            self.entry_icon.insert(0, filepath)

    def apply_preset(self, event=None):
        sel = self.preset_var.get()
        self.txt_message.delete("1.0", tk.END)
        self.entry_title.delete(0, tk.END)

        if sel == "Hydration Break":
            self.entry_title.insert(0, "💧 Hydration Alert")
            self.txt_message.insert("1.0", "Take a break and drink a glass of water!")
        elif sel == "Posture Check":
            self.entry_title.insert(0, "🪑 Posture Check")
            self.txt_message.insert( "1.0", "Sit up straight, roll your shoulders, and breathe.")
        elif sel == "Eye Rest (20-20-20)":
            self.entry_title.insert(0, "👀 Eye Strain Guard")
            self.txt_message.insert("1.0", "Look 20 feet away at something for 20 seconds.")
        elif sel == "Meeting Reminder":
            self.entry_title.insert(0, "📅 Meeting Notice")
            self.txt_message.insert("1.0", "Your scheduled meeting is about to begin.")

    def log_history(self, title, msg):
        now = datetime.now().strftime("%H:%M:%S")
        self.history_tree.insert("", 0, values=(now, title, msg))

    def export_history(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("--- DESKTOP NOTIFICATION HISTORY LOG ---\n\n")
                    for item_id in self.history_tree.get_children():
                        row = self.history_tree.item(item_id)["values"]
                        f.write(f"[{row[0]}] {row[1]}: {row[2]}\n")
                messagebox.สำเร็จ("Success", "History exported successfully!") if hasattr(messagebox, "สำเร็จ") else messagebox.showinfo("Success", "History exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")

    def send_desktop_notification(self, title, message, timeout, icon_path):
        kwargs = {"title": title, "message": message, "timeout": int(timeout)}
        if icon_path and os.path.exists(icon_path):
            kwargs["app_icon"] = icon_path

        if self.chk_sound_var.get():
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                self.root.bell()

        notification.notify(**kwargs)
        self.root.after(0, self.log_history, title, message)

    def notification_worker(self, title, message, timeout, delay, is_recurring, icon_path):
        while True:
            if delay > 0:
                time.sleep(delay)
            self.send_desktop_notification(title, message, timeout, icon_path)
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
            messagebox.showerror("Invalid Input", "Timeout and Delay must be valid numbers.")
            return

        if not title or not message:
            messagebox.showwarning("Missing Data", "Title and Message fields cannot be blank.")
            return

        is_recurring = self.chk_repeat_var.get()
        if is_recurring and delay <= 0:
            messagebox.showwarning("Loop Error", "Set a delay interval greater than 0 for loops.")
            return

        self.recurring_active = True
        threading.Thread(
            target=self.notification_worker,
            args=(title, message, timeout, delay, is_recurring, icon_path),
            daemon=True
        ).start()

        if delay > 0:
            messagebox.showinfo("Scheduled", f"Notification scheduled in {delay} seconds.")
        else:
            messagebox.showinfo("Success", "Notification sent successfully!")

    def stop_recurring(self):
        if self.recurring_active:
            self.recurring_active = False
            messagebox.showinfo("Stopped", "Recurring loops deactivated.")
        else:
            messagebox.showinfo("Info", "No active loop running.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDesktopNotifier(root)
    root.mainloop()