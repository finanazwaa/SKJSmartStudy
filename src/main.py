import tkinter as tk
from tkinter import messagebox
import os
import threading
import time
from datetime import datetime, timedelta
import json
from colorama import Fore, Style
from capture_domain import get_domains
from blocklist_loader import load_blocklist
from detection_module import is_blocked
from logging_system import log_alert
from notification_system import notify

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
    """
    Monitors domains until the timer ends or monitoring is stopped.
    """
    global monitoring, end_time
    blocklist = load_blocklist(config["blocklist"])  # Load the blocklist once
    while monitoring and datetime.now() < end_time:
        for domain in get_domains():
            if not monitoring:
                break
            process_domain(domain, blocklist)
        time.sleep(1)  # Add a small delay to avoid excessive CPU usage

    if monitoring:
        messagebox.showinfo("Info", "Monitoring complete!")
        generate_summary()
    monitoring = False

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
    print("generate_summary called")  # Debugging statement
    most_blocked = max(stats["blocked_domains"], key=stats["blocked_domains"].get, default="None")
    summary = (
        "----- DAILY SUMMARY -----\n"
        f"Total domains scanned: {stats['total']}\n"
        f"Blocked: {stats['blocked']}\n"
        f"Most blocked: {most_blocked}\n"
        "-------------------------\n"
    )
    print("Summary content:", summary)  # Debugging statement

    # Write the summary to a file
    with open("logs/daily_summary.txt", "w") as f:
        f.write(summary)

    # Display the summary in the GUI
    display_summary(summary)

def display_summary(summary):
    """
    Updates the summary text box in the GUI with the given summary.
    """
    print("display_summary called")  
    summary_text.config(state="normal")  
    summary_text.delete(1.0, tk.END)  
    summary_text.insert(tk.END, summary)  # Insert the new summary
    summary_text.config(state="disabled")  # Disable editing againext box
    summary_text.delete(1.0, tk.END)  # Clear previous content
    summary_text.insert(tk.END, summary)  # Insert the new summary
    summary_text.config(state="disabled")  # Disable editing again

# Create the GUI
root = tk.Tk()
root.title("Network Monitor")

# Duration input
tk.Label(root, text="Enter duration (minutes):", font=("Arial", 12)).pack(pady=5)
duration_entry = tk.Entry(root, font=("Arial", 12), justify="center")
duration_entry.pack(pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Start Monitoring", command=start_monitoring, bg="green", fg="white", font=("Arial", 10), width=15).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Stop Monitoring", command=stop_monitoring, bg="red", fg="white", font=("Arial", 10), width=15).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="View Logs", command=view_logs, bg="blue", fg="white", font=("Arial", 10), width=15).grid(row=1, column=0, pady=5)
tk.Button(button_frame, text="Edit Blocklist", command=edit_blocklist, bg="orange", fg="white", font=("Arial", 10), width=15).grid(row=1, column=1, pady=5)

# Summary Section
summary_label = tk.Label(root, text="Monitoring Summary", font=("Arial", 14, "bold"))
# Summary Section
summary_label = tk.Label(root, text="Monitoring Summary", font=("Arial", 14, "bold"))
summary_label.pack(pady=10)

summary_text = tk.Text(root, height=10, width=50, font=("Courier", 10), state="disabled", bg="#f4f4f4", fg="black")
summary_text.pack(pady=5)

# Function to display the summary in the GUI
def display_summary(summary):
    summary_text.config(state="normal")
    summary_text.delete(1.0, tk.END)  # Clear previous content
    summary_text.insert(tk.END, summary)
    summary_text.config(state="disabled")

# Run the GUI
root.mainloop()
