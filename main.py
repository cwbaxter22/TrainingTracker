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
# NAME + TAB LABEL HELPERS
# -------------------------
def extract_name(raw_text):
    """Best-effort name extraction from the pasted report text."""
    lines = [ln.strip() for ln in raw_text.splitlines()]

    # Preferred pattern: header line with "Safety Training Report" followed by name on next non-empty line
    for idx, line in enumerate(lines):
        if "Safety Training Report" in line:
            for follower in lines[idx + 1:]:
                if follower:
                    return follower
            break

    # Fallback: first non-empty line, minus header prefix if present
    for line in lines:
        if not line:
            continue
        if "Safety Training Report" in line:
            remainder = line.split("Safety Training Report", 1)[1].strip()
            if remainder:
                return remainder
            continue
        return line

    return None


def format_tab_label(name, passed):
    dot = "🟢" if passed else "🔴"
    if not name:
        return f"{dot} Tab"

    parts = name.split()
    if len(parts) >= 2:
        label = f"{parts[0][0]}. {parts[-1]}"
    else:
        label = parts[0]

    return f"{dot} {label}"


# -------------------------
# GUI CALLBACK
# -------------------------
def run_check(tab_widgets):
    text = tab_widgets["input_text"].get("1.0", tk.END)
    results = check_trainings(text)

    # Clear previous results for this tab
    for row in tab_widgets["results_frame"].winfo_children():
        row.destroy()
    tab_widgets["missing_list"].delete(0, tk.END)

    # Populate table
    for i, training in enumerate(REQUIRED_TRAININGS):
        status = results[training]

        symbol = "■" if status else "✖"
        color = "green" if status else "red"

        tk.Label(
            tab_widgets["results_frame"],
            text=symbol,
            fg=color,
            font=("Arial", 14, "bold"),
            width=2
        ).grid(row=i, column=0, padx=5, pady=2)

        tk.Label(
            tab_widgets["results_frame"],
            text=training,
            anchor="w",
            width=60
        ).grid(row=i, column=1, sticky="w")

        if not status:
            tab_widgets["missing_list"].insert(tk.END, training)

    all_passed = all(results.values()) if results else False
    name = extract_name(text)
    tab_label = format_tab_label(name, all_passed)
    notebook.tab(tab_widgets["frame"], text=tab_label)


# -------------------------
# GUI SETUP
# -------------------------
root = tk.Tk()
root.title("Safety Training Checker")
root.geometry("980x740")

top_bar = tk.Frame(root)
top_bar.pack(fill="x", pady=(8, 0), padx=10)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

tabs = []


def create_tab(title=None):
    index = len(tabs) + 1
    initial_title = title or f"Tab {index}"

    frame = ttk.Frame(notebook, padding=10)

    tk.Label(frame, text="Paste full training page text below:", font=("Arial", 11, "bold")).pack(anchor="w", pady=5)

    input_text = tk.Text(frame, height=15, wrap="word")
    input_text.pack(fill="x")

    tab_widgets = {
        "frame": frame,
        "input_text": input_text,
        "results_frame": None,
        "missing_list": None,
    }

    tk.Button(
        frame,
        text="Check Trainings",
        command=lambda: run_check(tab_widgets),
        font=("Arial", 11, "bold")
    ).pack(pady=10)

    tk.Label(frame, text="Training Status:", font=("Arial", 11, "bold")).pack(anchor="w")
    results_frame = tk.Frame(frame)
    results_frame.pack(anchor="w", padx=10, pady=5)

    tk.Label(frame, text="User is missing:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 0))
    missing_list = tk.Listbox(frame, width=80, height=6)
    missing_list.pack(padx=10, pady=5, anchor="w")

    tab_widgets["results_frame"] = results_frame
    tab_widgets["missing_list"] = missing_list

    notebook.add(frame, text=initial_title)
    tabs.append(tab_widgets)
    notebook.select(frame)


def add_tab():
    create_tab()


tk.Button(top_bar, text="➕ New Tab", command=add_tab, font=("Arial", 11, "bold")).pack(side="left")

# Start with one tab
create_tab()

root.mainloop()
