import tkinter as tk
from tkinter import ttk

# -------------------------
# REQUIRED TRAININGS (ORDER MATTERS)
# -------------------------
REQUIRED_TRAININGS = [
    "Electrical Safety Awareness Online",
    "Fire Extinguisher Training Online",
    "Asbestos General Awareness Online",
    "Ladder Safety Online",
    "Lockout Tagout Awareness Online",
    "Confined Space Entry Awareness Online",
    "Lead Awareness Online",
    "Globally Harmonized System for Hazard Communication Online",
    "Managing Laboratory Chemicals Online",
]

# -------------------------
# CORE PARSING FUNCTION
# -------------------------
def check_trainings(pasted_text):
    results = {}

    lines = pasted_text.splitlines()

    for training in REQUIRED_TRAININGS:
        found_current = False
        for line in lines:
            if training in line and "Current" in line:
                found_current = True
                break
        results[training] = found_current

    return results

# -------------------------
# GUI CALLBACK
# -------------------------
def run_check():
    text = input_text.get("1.0", tk.END)
    results = check_trainings(text)

    # Clear previous results
    for row in results_frame.winfo_children():
        row.destroy()
    missing_list.delete(0, tk.END)

    # Populate table
    for i, training in enumerate(REQUIRED_TRAININGS):
        status = results[training]

        symbol = "■" if status else "✖"
        color = "green" if status else "red"

        tk.Label(
            results_frame,
            text=symbol,
            fg=color,
            font=("Arial", 14, "bold"),
            width=2
        ).grid(row=i, column=0, padx=5, pady=2)

        tk.Label(
            results_frame,
            text=training,
            anchor="w",
            width=60
        ).grid(row=i, column=1, sticky="w")

        if not status:
            missing_list.insert(tk.END, training)

# -------------------------
# GUI SETUP
# -------------------------
root = tk.Tk()
root.title("Safety Training Checker")
root.geometry("900x700")

# Input label
tk.Label(root, text="Paste full training page text below:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=5)

# Text input
input_text = tk.Text(root, height=15, wrap="word")
input_text.pack(fill="x", padx=10)

# Button
tk.Button(root, text="Check Trainings", command=run_check, font=("Arial", 11, "bold")).pack(pady=10)

# Results table
tk.Label(root, text="Training Status:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
results_frame = tk.Frame(root)
results_frame.pack(anchor="w", padx=20, pady=5)

# Missing section
tk.Label(root, text="User is missing:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(20, 0))
missing_list = tk.Listbox(root, width=80, height=6)
missing_list.pack(padx=20, pady=5)

root.mainloop()
