import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pathlib import Path
from src.wipe import secure_delete_with_report, wipe_free_with_report
from src.utils import list_drives

# Browse file/folder
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)

# Preview free space
def preview():
    target = entry.get().strip()
    if not target:
        messagebox.showwarning("Warning", "Please select a folder first.")
        return
    try:
        wipe_free_with_report(Path(target), preview=True)
        messagebox.showinfo("Preview Complete", f"Previewed free space in:\n{target}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# Secure delete file/folder
def wipe():
    target = entry.get().strip()
    if not target:
        messagebox.showwarning("Warning", "Please select a file or folder first.")
        return
    try:
        secure_delete_with_report(Path(target), passes=3)
        messagebox.showinfo("Success", f"✅ File/folder securely deleted:\n{target}")
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"⚠️ An unexpected error occurred:\n{str(e)}")

# Show drives in text widget
def show_drives():
    drives = list_drives()
    drives_text.delete(1.0, tk.END)
    drives_text.insert(tk.END, "Available drives:\n")
    for d in drives:
        if isinstance(d, dict):
            drives_text.insert(tk.END, f" - {d['device']} ({d['mountpoint']}) - Free: {d['free']/(1024**3):.2f} GB\n")
        else:
            drives_text.insert(tk.END, f" - {d}\n")

# Wipe free space / USB GUI
def wipe_free_gui():
    removable_only = messagebox.askyesno("USB Only?", "Select only USB/removable drives?")
    drives = list_drives(only_removable=removable_only)
    if not drives:
        messagebox.showinfo("No Drives", "No drives found.")
        return

    select_win = tk.Toplevel(root)
    select_win.title("Select Drive/Folder to Wipe")

    tk.Label(select_win, text="Select a drive/folder to wipe free space:").pack(padx=10, pady=10)

    drive_var = tk.StringVar()
    options = [f"{d['device']} ({d['mountpoint']})" for d in drives]
    combo = ttk.Combobox(select_win, values=options, textvariable=drive_var, width=50)
    combo.pack(padx=10, pady=5)
    combo.current(0)

    def start_wipe():
        target = drive_var.get().split('(')[1].rstrip(')')
        preview_choice = messagebox.askyesno("Preview", "Do you want to preview free space first?")
        try:
            wipe_free_with_report(Path(target), passes=1, preview=preview_choice)
            if not preview_choice:
                messagebox.showinfo("Done", f"Free space wipe completed on:\n{target}")
            select_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    tk.Button(select_win, text="Start Wipe", command=start_wipe).pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("Secure Deletion Tool")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

entry = tk.Entry(frame, width=50)
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

browse_file_btn = tk.Button(frame, text="Browse File", command=browse_file)
browse_file_btn.grid(row=1, column=0, padx=5, pady=5)

browse_folder_btn = tk.Button(frame, text="Browse Folder", command=browse_folder)
browse_folder_btn.grid(row=1, column=1, padx=5, pady=5)

preview_btn = tk.Button(frame, text="Preview Free Space", command=preview)
preview_btn.grid(row=1, column=2, padx=5, pady=5)

wipe_btn = tk.Button(frame, text="Secure Delete", command=wipe)
wipe_btn.grid(row=1, column=3, padx=5, pady=5)

drives_btn = tk.Button(frame, text="List Drives", command=show_drives)
drives_btn.grid(row=2, column=0, columnspan=2, pady=10)

wipe_free_btn = tk.Button(frame, text="Wipe Free Space / USB", command=wipe_free_gui)
wipe_free_btn.grid(row=2, column=2, columnspan=2, pady=10)

# Scrollable text widget for showing drives
drives_text = scrolledtext.ScrolledText(frame, width=60, height=10)
drives_text.grid(row=3, column=0, columnspan=4, pady=10)

root.mainloop()
