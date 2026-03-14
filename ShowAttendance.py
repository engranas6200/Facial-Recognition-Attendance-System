import sqlite3
from tkinter import *
from tkinter import ttk

# --- Database file ---
DB_FILE = 'face_attendance.db'

# --- Fetch all student records ---
def fetch_attendance():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, total_attendance, last_attendance_time FROM Students")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Tkinter UI ---
root = Tk()
root.title("Attendance Records")

# Treeview (table)
tree = ttk.Treeview(root, columns=("ID", "Name", "Total Attendance", "Last Attendance"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Total Attendance", text="Total Attendance")
tree.heading("Last Attendance", text="Last Attendance Time")

# Fill table with database data
for row in fetch_attendance():
    tree.insert("", END, values=row)

tree.pack(fill=BOTH, expand=True)

# Refresh button
def refresh():
    for i in tree.get_children():
        tree.delete(i)
    for row in fetch_attendance():
        tree.insert("", END, values=row)

Button(root, text="Refresh", command=refresh, bg="blue", fg="white").pack(pady=5)

root.mainloop()
