from repositories.program_repository import ProgramRepository

class ProgramService:
    """Service layer for program business logic"""
    
    def __init__(self):
        self.program_repo = ProgramRepository()
    
    def get_all_programs(self):
        """Get all programs"""
        programs = self.program_repo.get_all()
        
        # Transform to dict
        result = []
        for program in programs:
            result.append({
                'id': program['id'],
                'program_code': program['program_code'],
                'duration_years': program['duration_years']
            })
        
        return result
    
    def get_program_by_id(self, program_id):
        """Get a program by ID"""
        program = self.program_repo.get_by_id(program_id)
        
        if not program:
            return None
        
        return {
            'id': program['id'],
            'program_name': program['program_name'],
            'program_code': program['program_code'],
            'duration_years': program['duration_years']
        }
