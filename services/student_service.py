from repositories.student_repository import StudentRepository
from repositories.program_repository import ProgramRepository
from datetime import datetime

class StudentService:
    """Service layer for student business logic"""
    
    def __init__(self):
        self.student_repo = StudentRepository()
        self.program_repo = ProgramRepository()
    
    def get_all_students(self, page=1, per_page=10):
        """Get all students with pagination"""
        offset = (page - 1) * per_page
        students = self.student_repo.get_all(limit=per_page, offset=offset)
        total = self.student_repo.get_count()
        
        # Transform to dict
        result = []
        for student in students:
            result.append({
                'id': student['id'],
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'full_name': f"{student['first_name']} {student['last_name']}",
                'email': student['email'],
                'enrollment_date': student['enrollment_date'],
                'program_code': student['program_code'],
                'program_name': student['program_name']
            })
        
        return {
            'items': result,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    
    def get_student_by_id(self, student_id):
        """Get a student by ID with program details"""
        student = self.student_repo.get_by_id(student_id)
        
        if not student:
            return None
        
        return {
            'id': student['id'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'full_name': f"{student['first_name']} {student['last_name']}",
            'email': student['email'],
            'enrollment_date': student['enrollment_date'],
            'program': {
                'program_code': student['program_code'],
                'program_name': student['program_name'],
                'duration_years': student['duration_years']
            }
        }
    
    def create_student(self, first_name, last_name, email, program_code, enrollment_date=None):
        """Create a new student"""
        # Validate program exists
        if not self.program_repo.exists(program_code):
            raise ValueError('Program not found')
        
        # Generate student ID
        student_id = self.student_repo.get_next_id()
        
        # Use current date if not provided
        if not enrollment_date:
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
        
        # Create student
        self.student_repo.create(student_id, first_name, last_name, email, enrollment_date, program_code)
        
        return {
            'id': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'enrollment_date': enrollment_date,
            'program_code': program_code
        }
    
    def update_student(self, student_id, first_name=None, last_name=None, email=None, enrollment_date=None, program_code=None):
        """Update a student"""
        # Check if student exists
        if not self.student_repo.exists(student_id):
            return None
        
        # Validate program if provided
        if program_code and not self.program_repo.exists(program_code):
            raise ValueError('Program not found')
        
        # Update student
        self.student_repo.update(student_id, first_name, last_name, email, enrollment_date, program_code)
        
        # Return updated student
        return self.get_student_by_id(student_id)
    
    def delete_student(self, student_id):
        """Delete a student"""
        if not self.student_repo.exists(student_id):
            return False
        
        self.student_repo.delete(student_id)
        return True
    
    def validate_student_data(self, data):
        """Validate student data"""
        errors = []
        
        if not data.get('first_name'):
            errors.append('first_name is required')
        if not data.get('last_name'):
            errors.append('last_name is required')
        if not data.get('email'):
            errors.append('email is required')
        if not data.get('program_code'):
            errors.append('program_code is required')
        
        return errors
