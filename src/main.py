import tkinter as tk
from tkinter import messagebox, ttk
import threading
from datetime import datetime, timedelta
import os
import time
import json
from blocklist_loader import load_blocklist
from detection_module import is_blocked
from logging_system import log_alert
from notification_system import notify
from capture_domain import get_domains

# Load configuration from config.json
config = json.load(open("config.json"))

# Global variables
monitoring = False
end_time = None

# Initialize stats dictionary
stats = {
    "total": 0,
    "blocked": 0,
    "blocked_domains": {}
}

def start_monitoring():
    """
    Starts the monitoring process.
    """
    global monitoring, end_time
    if monitoring:
        messagebox.showinfo("Info", "Monitoring is already running!")
        return

    try:
        duration_minutes = int(duration_entry.get())
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        monitoring = True
        messagebox.showinfo("Info", f"Monitoring started for {duration_minutes} minutes!")
        threading.Thread(target=monitor_domains).start()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of minutes.")

def stop_monitoring():
    """
    Stops the monitoring process.
    """
    global monitoring
    if not monitoring:
        messagebox.showinfo("Info", "Monitoring is not running!")
        return

    monitoring = False
    messagebox.showinfo("Info", "Monitoring stopped!")

def monitor_domains():
    global monitoring, end_time  # <-- FIX HERE

    blocklist = load_blocklist(config["blocklist"])  # Load the blocklist once
    domains = get_domains()[:100]  # Limit to the first 100 domains
    print(f"Domains to process: {domains}")  # Debugging statement
    print(f"Blocklist: {blocklist}")  # Debugging statement

    while monitoring and datetime.now() < end_time:
        for domain in domains:
            if not monitoring:
                break
            process_domain(domain, blocklist)
            update_stats()  # Update stats in the GUI
        time.sleep(1)  # Add a small delay to avoid excessive CPU usage

    if monitoring:
        generate_summary()
    monitoring = False

def update_progress_bar(value):
    """Updates progress bar in GUI"""
    progress_bar["value"] = value

def update_stats():
    """
    Updates the stats section in the GUI.
    """
    total_label.config(text=f"Total Domains Scanned: {stats['total']}")
    blocked_label.config(text=f"Blocked Domains: {stats['blocked']}")
    progress_bar["value"] = min(stats["total"], 100)  # Fixed progress calculation

def view_logs():
    """
    Opens the logs file in the default text editor.
    """
    log_path = config["log_path"]
    if os.path.exists(log_path):
        os.system(f"open {log_path}" if os.name == "posix" else f"start {log_path}")
    else:
        messagebox.showerror("Error", "Log file not found!")

def edit_blocklist():
    """
    Opens the blocklist file in the default text editor.
    """
    blocklist_path = config["blocklist"]
    if os.path.exists(blocklist_path):
        os.system(f"open {blocklist_path}" if os.name == "posix" else f"start {blocklist_path}")
    else:
        messagebox.showerror("Error", "Blocklist file not found!")

def process_domain(domain, blocklist):
    """
    Processes a single domain to check if it is blocked, logs an alert, and sends a notification.

    Args:
        domain (str): The domain to process.
        blocklist (list): The preloaded blocklist.
    """
    stats["total"] += 1
    if is_blocked(domain, blocklist):
        stats["blocked"] += 1
        stats["blocked_domains"][domain] = stats["blocked_domains"].get(domain, 0) + 1
        log_alert(domain)
        if config["notifications"]:
            notify(domain)

def generate_summary():
    """
    Generates a daily summary and writes it to a text file.
    """
    most_blocked = max(stats["blocked_domains"], key=stats["blocked_domains"].get, default="None")
    summary = (
        "----- DAILY SUMMARY -----\n"
        f"Total domains scanned: {stats['total']}\n"
        f"Blocked: {stats['blocked']}\n"
        f"Most blocked: {most_blocked}\n"
        "-------------------------\n"
    )
    with open("logs/daily_summary.txt", "w") as f:
        f.write(summary)
    display_summary(summary)

    # Schedule the messagebox in the main thread using `after`
    root.after(0, lambda: messagebox.showinfo("Info", "Summary saved to logs/daily_summary.txt!"))

def display_summary(summary):
    """
    Updates the summary text box in the GUI with the given summary.
    """
    summary_text.config(state="normal")
    summary_text.delete(1.0, tk.END)
    summary_text.insert(tk.END, summary)
    summary_text.config(state="disabled")

# Create the GUI
root = tk.Tk()
root.title("Interactive Network Monitor")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

# Title
title_label = tk.Label(root, text="Network Monitor", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

# Duration input
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter duration (minutes):", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
duration_entry = tk.Entry(input_frame, font=("Arial", 12), justify="center")
duration_entry.grid(row=0, column=1, padx=5)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Start Monitoring", command=start_monitoring, bg="green", fg="white", font=("Arial", 10), width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Stop Monitoring", command=stop_monitoring, bg="red", fg="white", font=("Arial", 10), width=15).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="View Logs", command=view_logs, bg="blue", fg="white", font=("Arial", 10), width=15).grid(row=1, column=0, pady=5)
tk.Button(button_frame, text="Edit Blocklist", command=edit_blocklist, bg="orange", fg="white", font=("Arial", 10), width=15).grid(row=1, column=1, pady=5)

# Stats Section
stats_frame = tk.Frame(root, bg="#f0f0f0")
stats_frame.pack(pady=10)

total_label = tk.Label(stats_frame, text="Total Domains Scanned: 0", font=("Arial", 12), bg="#f0f0f0", fg="#333")
total_label.grid(row=0, column=0, padx=5)

blocked_label = tk.Label(stats_frame, text="Blocked Domains: 0", font=("Arial", 12), bg="#f0f0f0", fg="#333")
blocked_label.grid(row=1, column=0, padx=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Summary Section
summary_label = tk.Label(root, text="Monitoring Summary", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333")
summary_label.pack(pady=10)

summary_text = tk.Text(root, height=10, width=60, font=("Courier", 10), state="disabled", bg="#ffffff", fg="black")
summary_text.pack(pady=5)

# Run the GUI
root.mainloop()


# run python3 main.py in command line to test the code
