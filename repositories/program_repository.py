from .base_repository import BaseRepository

class ProgramRepository(BaseRepository):
    """Repository for program data access"""
    
    def get_all(self):
        """Get all programs"""
        query = 'SELECT program_code, program_name, duration_years FROM programs ORDER BY program_code'
        return self.execute_query(query)
    
    def get_by_code(self, program_code):
        """Get a program by program_code"""
        query = 'SELECT program_code, program_name, duration_years FROM programs WHERE program_code = ?'
        return self.execute_one(query, (program_code,))
    
    def exists(self, program_code):
        """Check if a program exists"""
        query = 'SELECT program_code FROM programs WHERE program_code = ?'
        result = self.execute_one(query, (program_code,))
        return result is not None
