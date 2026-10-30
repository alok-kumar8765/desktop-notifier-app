# ⚡ Modern Glossy Desktop Notifier

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Stars](https://img.shields.io/github/stars/alok--kumar8765/desktop-notifier-app?style=social)

A sleek, modern, multi-themed desktop notification manager built with Python. Designed for productivity, wellness reminders, and custom task scheduling—without the bloat of unstable third-party GUI frameworks.

---

## 📑 Table of Contents
1. [Purpose & Use Cases](#-purpose--use-cases)
2. [Key Features](#-key-features)
3. [System Requirements](#-system-requirements)
4. [Installation & Setup](#-installation--setup)
5. [File Structure](#-file-structure)
6. [Architecture & Diagrams](#-architecture--diagrams)
   - [Data Flow Diagram (DFD)](#data-flow-diagram-dfd)
   - [Entity Relationship (ER) Diagram](#entity-relationship-er-diagram)
7. [Pros & Cons](#-pros--cons)
8. [Limitations](#-limitation)
9. [Bugs & Vulnerabilities](#-known-bugs--vulnerabilities)
10. [Future Roadmap](#-future-updates)
11. [Contributing](#-contributing)
12. [Acknowledgments & Support](#-acknowledgments--support)

---

## 🎯 Purpose & Use Cases

### Purpose
The **Modern Glossy Desktop Notifier** provides an offline, lightweight, and customizable desktop alert system. It bridges the gap between simple command-line alert scripts and heavy desktop utilities.

### Primary Use Cases
* **Health & Wellness Alerts:** Automated reminders for drinking water, taking posture breaks, and applying the 20-20-20 eye strain rule.
* **Productivity & Focus:** Interval-based countdown timers for the Pomodoro technique.
* **System Alerts:** Customized event notifications with system audio chimes.

---

## ✨ Key Features

* 🎨 **Multi-Theme Engine:** Real-time theme switcher featuring *Dark Glossy*, *Light Modern*, and *Cyberpunk Neon*.
* 🚀 **Multi-Threaded Execution:** Background scheduling using Python `threading` prevents GUI freezing during long countdowns.
* ⚡ **Preset Workflows:** Instant notification presets for health, meetings, and daily tasks.
* ⏳ **Flexible Timers & Recurring Loops:** Schedule alerts for a future delay or put them on an automated repeat cycle.
* 🔊 **Audio Feedback:** Integrated system audio chime alerts.
* 🖼️ **Custom Branding:** Support for custom application `.ico` icons.
* 📜 **Notification Log:** Interactive history tracker with export capabilities to `.txt` files.

---

## 💻 System Requirements

* **Operating System:** Windows 10/11, macOS, or Linux
* **Python Version:** Python 3.8 or higher
* **Dependencies:** `plyer`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alok--kumar8765/desktop-notifier-app.git
cd desktop-notifier-app
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install plyer
```

### 4. Run the Application
```bash
python advanced_notifier.py
```

---

## 📁 File Structure

```
desktop-notifier-app/
│
├── advanced_notifier.py   # Main application source code
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies list
└── assets/                # Folder for custom icons (.ico) and media
    └── default_icon.ico
```

---

## 📐 Architecture & Diagrams

### Data Flow Diagram (DFD)

```
 +------------------+          +------------------------+          +-----------------------+
 |                  | -------->|  Validate Form Data    | -------->| Background Thread     |
 |  User Interface  |          |  (Title, Msg, Delay)   |          | (Timer Countdown)     |
 |  (Tkinter GUI)   |          +------------------------+          +-----------------------+
 |                  |                                                          |
 |                  | <--------------------------------------------------------+
 +------------------+                                                          |
          |                                                                    v
          |                                                       +-----------------------+
          |                                                       | Trigger System Alert  |
          |                                                       | (Plyer & Audio Sound) |
          v                                                       +-----------------------+
 +------------------+                                                          |
 | History Treeview | <--------------------------------------------------------+
 | Log Database     |
 +------------------+
```

### Entity Relationship (ER) Diagram

```
+-----------------------------------+        1 : N        +-----------------------------------+
|            SETTINGS               | ------------------> |           NOTIFICATION            |
+-----------------------------------+                     +-----------------------------------+
| PK : theme_id                     |                     | PK : notification_id              |
|      theme_name (String)          |                     |      title (String)               |
|      bg_color (Hex)               |                     |      message_body (Text)          |
|      accent_color (Hex)           |                     |      timeout_seconds (Int)        |
|      play_sound (Boolean)         |                     |      scheduled_delay (Int)        |
+-----------------------------------+                     |      is_recurring (Boolean)       |
                                                          |      icon_path (FilePath)         |
                                                          +-----------------------------------+
                                                                            |
                                                                            | 1 : N
                                                                            v
                                                          +-----------------------------------+
                                                          |            HISTORY_LOG            |
                                                          +-----------------------------------+
                                                          | PK : log_id                       |
                                                          | FK : notification_id              |
                                                          |      timestamp (DateTime)         |
                                                          |      status (Sent/Failed)         |
                                                          +-----------------------------------+
```

---

## ⚖️ Pros & Cons

### Pros
* **High Stability:** Uses built-in `tkinter` to eliminate crash risks associated with external wrapper libraries.
* **Non-Blocking UI:** Smooth user experience powered by asynchronous background threading.
* **Low Resource Usage:** Minimal CPU and RAM footprint (< 30 MB RAM).

### Cons
* **No Native Tray Minimization:** Requires additional external libraries (`pystray`) to minimize to the system tray.
* **Basic Text Exporting:** Native log exporting is limited to plain text (`.txt`) rather than relational databases.

---

## 🛑 Limitation

* **Platform Specific Icons:** `.ico` format is strictly required for Windows desktop notifications; `.png` or `.icns` are required on Linux/macOS.
* **In-Memory Storage:** History logs reset upon closing the app unless manually exported.

---

## 🐛 Known Bugs & Vulnerabilities

* **System Bell Fallback:** On certain Linux distributions without a configured system bell, audio chimes may fail silently.
* **Thread Accumulation:** Rapidly firing multiple recurring threads without stopping previous ones can increase background CPU threads.

---

## 🔮 Future Updates

* [ ] Add System Tray integration via `pystray`.
* [ ] Persistent local storage via SQLite database.
* [ ] CSV/JSON export options for logs.
* [ ] External REST API integration for Live Weather & Stock alert feeds.

---

## 🤝 Contributing

Contributions are always welcome!

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/AwesomeFeature`).
3. Commit your Changes (`git commit -m 'Add some AwesomeFeature'`).
4. Push to the Branch (`git push origin feature/AwesomeFeature`).
5. Open a Pull Request.

---

## ⭐ Acknowledgments & Support

If you found this project helpful, please give it a **⭐ Star** on GitHub!

* Created with ❤️ by [@alok--kumar8765](https.github.com/alok--kumar8765)
* Powered by [Plyer](https://github.com/kivy/plyer)