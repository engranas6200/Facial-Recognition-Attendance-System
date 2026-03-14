import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from datetime import datetime
import cv2
import face_recognition
import pickle
import os
import numpy as np

def add_student():
    student_id = entry_id.get()
    name = entry_name.get()
    major = entry_major.get()
    year = int(entry_year.get())
    photo_path = photo_file_path.get()

    if not all([student_id, name, major, year, photo_path]):
        messagebox.showerror("Error", "All fields are required")
        return

    # Save photo to Images folder
    folderPath = r'C:\Users\engra\Desktop\Marghoob saab ka proect\Files\Images' 
    os.makedirs(folderPath, exist_ok=True)
    ext = os.path.splitext(photo_path)[1]
    dest_path = os.path.join(folderPath, f"{student_id}{ext}")
    cv2.imwrite(dest_path, cv2.imread(photo_path))

    # Update database
    conn = sqlite3.connect("face_attendance.db")
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, name, major, year, 0, "A", year, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    # Update face encodings
    img = cv2.imread(dest_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img_rgb)[0]

    if os.path.exists("EncodeFile.p"):
        with open("EncodeFile.p", "rb") as f:
            encode_list, ids = pickle.load(f)
    else:
        encode_list, ids = [], []

    encode_list.append(encode)
    ids.append(student_id)
    with open("EncodeFile.p", "wb") as f:
        pickle.dump([encode_list, ids], f)

    messagebox.showinfo("Success", f"Student {name} added!")

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    photo_file_path.set(path)

# GUI
root = tk.Tk()
root.title("Face Attendance System")

tk.Label(root, text="Roll No").grid(row=0, column=0)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1)

tk.Label(root, text="Name").grid(row=1, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

tk.Label(root, text="Major").grid(row=2, column=0)
entry_major = tk.Entry(root)
entry_major.grid(row=2, column=1)

tk.Label(root, text="Year").grid(row=3, column=0)
entry_year = tk.Entry(root)
entry_year.grid(row=3, column=1)

photo_file_path = tk.StringVar()
tk.Button(root, text="Upload Photo", command=browse_file).grid(row=4, column=0)
tk.Entry(root, textvariable=photo_file_path).grid(row=4, column=1)

tk.Button(root, text="Add Student", command=add_student).grid(row=5, column=0, columnspan=2)

root.mainloop()
