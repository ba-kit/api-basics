import sqlite3
from datetime import datetime, timedelta
import random
import os

DATABASE_NAME = os.environ.get('DATABASE_PATH', 'students.db')

def get_connection():
    """Get a database connection - SQLite doesn't need connection pooling"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS programs')
    
    cursor.execute('''
        CREATE TABLE programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL,
            program_code TEXT NOT NULL UNIQUE,
            duration_years INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE students (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            enrollment_date TEXT NOT NULL,
            program_id INTEGER NOT NULL,
            FOREIGN KEY (program_id) REFERENCES programs (id)
        )
    ''')
    
    # Create index for faster student ID lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_id ON students(id)')
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    programs = [
        ('Certificate IV in Information Technology', 'ICT40120', 1),
        ('Diploma of Software Development', 'ICT50220', 2),
        ('Advanced Diploma of Network Security', 'ICT60220', 2),
        ('Certificate III in Business', 'BSB30120', 1),
        ('Diploma of Project Management', 'BSB50820', 2),
        ('Certificate IV in Design', 'CUA40720', 1),
        ('Diploma of Graphic Design', 'CUA50720', 2),
        ('Certificate IV in Accounting and Bookkeeping', 'FNS40217', 1),
        ('Diploma of Leadership and Management', 'BSB50420', 2),
        ('Advanced Diploma of Engineering Technology', 'MEM60212', 3)
    ]
    
    cursor.executemany(
        'INSERT INTO programs (program_name, program_code, duration_years) VALUES (?, ?, ?)',
        programs
    )
    
    first_names = ['Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'William', 'Sophia', 'James', 'Isabella', 'Oliver',
                   'Charlotte', 'Benjamin', 'Amelia', 'Lucas', 'Mia', 'Henry', 'Harper', 'Alexander', 'Evelyn', 'Michael']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    students = []
    base_date = datetime.now() - timedelta(days=365)
    
    for i in range(20):
        first_name = first_names[i]
        last_name = last_names[i]
        email = f"{first_name.lower()}.{last_name.lower()}@student.tafe.edu.au"
        enrollment_date = (base_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        program_id = random.randint(1, 10)
        student_id = f"ACT{(i+1):03d}"
        
        students.append((student_id, first_name, last_name, email, enrollment_date, program_id))
    
    cursor.executemany(
        'INSERT INTO students (id, first_name, last_name, email, enrollment_date, program_id) VALUES (?, ?, ?, ?, ?, ?)',
        students
    )
    
    conn.commit()
    conn.close()
    print(f"Seeded {len(programs)} programs and {len(students)} students!")

def reset_database():
    print("Resetting database...")
    init_database()
    seed_data()
    print("Database reset complete!")

if __name__ == '__main__':
    reset_database()
