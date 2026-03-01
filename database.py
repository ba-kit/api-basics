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
            program_code TEXT PRIMARY KEY,
            program_name TEXT NOT NULL,
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
            program_code TEXT NOT NULL,
            FOREIGN KEY (program_code) REFERENCES programs (program_code)
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
        ('ICT40120', 'Certificate IV in Information Technology', 1),
        ('ICT50220', 'Diploma of Software Development', 2),
        ('ICT60220', 'Advanced Diploma of Network Security', 2),
        ('BSB30120', 'Certificate III in Business', 1),
        ('BSB50820', 'Diploma of Project Management', 2),
        ('CUA40720', 'Certificate IV in Design', 1),
        ('CUA50720', 'Diploma of Graphic Design', 2),
        ('FNS40217', 'Certificate IV in Accounting and Bookkeeping', 1),
        ('BSB50420', 'Diploma of Leadership and Management', 2),
        ('MEM60212', 'Advanced Diploma of Engineering Technology', 3)
    ]
    
    program_codes = [p[0] for p in programs]
    
    cursor.executemany(
        'INSERT INTO programs (program_code, program_name, duration_years) VALUES (?, ?, ?)',
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
        program_code = random.choice(program_codes)
        student_id = f"ACT{(i+1):03d}"
        
        students.append((student_id, first_name, last_name, email, enrollment_date, program_code))
    
    cursor.executemany(
        'INSERT INTO students (id, first_name, last_name, email, enrollment_date, program_code) VALUES (?, ?, ?, ?, ?, ?)',
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
