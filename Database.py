import sqlite3
from sqlite3 import Error
from datetime import datetime

DATABASE = "face_attendance.db"

def create_connection():
    """Create a connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(f"Database error: {e}")
    return conn

def create_table():
    """Create the students table"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        major TEXT,
        starting_year INTEGER,
        total_attendance INTEGER DEFAULT 0,
        standing TEXT,
        year INTEGER,
        last_attendance_time TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_student(student_id, name, major, starting_year, total_attendance=0, standing="N/A", year=1, last_attendance_time=None):
    conn = create_connection()
    cursor = conn.cursor()
    if last_attendance_time is None:
        last_attendance_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT OR REPLACE INTO students (id, name, major, starting_year, total_attendance, standing, year, last_attendance_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_id, name, major, starting_year, total_attendance, standing, year, last_attendance_time))
    conn.commit()
    conn.close()

def get_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        keys = ["id", "name", "major", "starting_year", "total_attendance", "standing", "year", "last_attendance_time"]
        return dict(zip(keys, row))
    return None

def update_attendance(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    student = get_student(student_id)
    if student:
        last_time = datetime.strptime(student['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
        secondsElapsed = (datetime.now() - last_time).total_seconds()
        if secondsElapsed > 30:
            new_total = student['total_attendance'] + 1
            cursor.execute("UPDATE students SET total_attendance=?, last_attendance_time=? WHERE id=?",
                           (new_total, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), student_id))
            conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Database and table created successfully!")



