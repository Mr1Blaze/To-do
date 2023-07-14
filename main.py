import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
        save_task(task)
    else:
        messagebox.showwarning("Warning", "You need te write a task!")


def delete_task():
    try:
        index = listbox.curselection()
        selected_task = listbox.get(index)
        listbox.delete(index)
        delete_task_from_db(selected_task)
    except:
        messagebox.showwarning("Warning ", "You need to select task to delete")


def save_task(task):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()


def delete_task_from_db(task):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE task=?", (task,))
    conn.commit()
    conn.close()


def load_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    for row in rows:
        listbox.insert(tk.END, row[0])
    conn.close()


window = tk.Tk()
window.title("To-Do app")

window_style = ttk.Style()
window_style.configure("TFrame", background="#e1d8b9")
window_style.configure("TButton", background="#b1a296", foreground="white", font=("Helvetica", 12, "bold"))
window_style.configure("TLabel", background="#e1d8b9", foreground="#555555", font=("Helvetica", 12))
window_style.configure("TEntry", font=("Helvetica", 12))

main_frame = ttk.Frame(window)
main_frame.pack(pady=10)

listbox = tk.Listbox(main_frame, height=10, width=50, font=("Helvetica", 12))
listbox.grid(row=0, column=0, padx=5, pady=5)

scrollbar = ttk.Scrollbar(main_frame)
scrollbar.grid(row=0, column=1, sticky="ns")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

entry = ttk.Entry(main_frame, font=("Helvetica", 12))
entry.grid(row=1, column=0, padx=5, pady=5)

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=2, column=0, padx=5, pady=5)

add_button = ttk.Button(button_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=0, padx=5)

delete_button = ttk.Button(button_frame, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=1, padx=5)

conn = sqlite3.connect("tasks.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tasks (task TEXT)")
conn.commit()
conn.close()
load_tasks()

window.mainloop()
