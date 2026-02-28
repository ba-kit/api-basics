from .base_repository import BaseRepository

class StudentRepository(BaseRepository):
    """Repository for student data access"""
    
    def get_all(self, limit=None, offset=None):
        """Get all students with optional pagination"""
        query = '''
            SELECT s.*, p.program_name, p.program_code, p.duration_years
            FROM students s
            JOIN programs p ON s.program_id = p.id
            ORDER BY s.id
        '''
        
        if limit:
            query += f' LIMIT {limit}'
        if offset:
            query += f' OFFSET {offset}'
        
        return self.execute_query(query)
    
    def get_by_id(self, student_id):
        """Get a student by ID"""
        query = '''
            SELECT s.*, p.id as program_id, p.program_name, p.program_code, p.duration_years
            FROM students s
            JOIN programs p ON s.program_id = p.id
            WHERE s.id = ?
        '''
        return self.execute_one(query, (student_id,))
    
    def get_count(self):
        """Get total count of students"""
        query = 'SELECT COUNT(*) as count FROM students'
        result = self.execute_one(query)
        return result['count'] if result else 0
    
    def create(self, student_id, first_name, last_name, email, enrollment_date, program_id):
        """Create a new student"""
        query = '''
            INSERT INTO students (id, first_name, last_name, email, enrollment_date, program_id)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.execute_write(query, (student_id, first_name, last_name, email, enrollment_date, program_id))
        return student_id
    
    def update(self, student_id, first_name=None, last_name=None, email=None, enrollment_date=None, program_id=None):
        """Update a student"""
        updates = []
        params = []
        
        if first_name:
            updates.append('first_name = ?')
            params.append(first_name)
        if last_name:
            updates.append('last_name = ?')
            params.append(last_name)
        if email:
            updates.append('email = ?')
            params.append(email)
        if enrollment_date:
            updates.append('enrollment_date = ?')
            params.append(enrollment_date)
        if program_id:
            updates.append('program_id = ?')
            params.append(program_id)
        
        if not updates:
            return False
        
        params.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
        self.execute_write(query, tuple(params))
        return True
    
    def delete(self, student_id):
        """Delete a student"""
        query = 'DELETE FROM students WHERE id = ?'
        self.execute_write(query, (student_id,))
        return True
    
    def get_next_id(self):
        """Get the next student ID in ACT format"""
        query = 'SELECT id FROM students WHERE id LIKE "ACT%" ORDER BY id DESC LIMIT 1'
        result = self.execute_one(query)
        
        if result:
            last_num = int(result['id'][3:])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f"ACT{new_num:03d}"
    
    def exists(self, student_id):
        """Check if a student exists"""
        query = 'SELECT id FROM students WHERE id = ?'
        result = self.execute_one(query, (student_id,))
        return result is not None
