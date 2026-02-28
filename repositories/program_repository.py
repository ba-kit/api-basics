from .base_repository import BaseRepository

class ProgramRepository(BaseRepository):
    """Repository for program data access"""
    
    def get_all(self):
        """Get all programs"""
        query = 'SELECT id, program_code, duration_years FROM programs ORDER BY program_code'
        return self.execute_query(query)
    
    def get_by_id(self, program_id):
        """Get a program by ID"""
        query = 'SELECT * FROM programs WHERE id = ?'
        return self.execute_one(query, (program_id,))
    
    def exists(self, program_id):
        """Check if a program exists"""
        query = 'SELECT id FROM programs WHERE id = ?'
        result = self.execute_one(query, (program_id,))
        return result is not None
