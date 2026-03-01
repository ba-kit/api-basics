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
                'program_code': program['program_code'],
                'program_name': program['program_name'],
                'duration_years': program['duration_years']
            })
        
        return result
    
    def get_program_by_code(self, program_code):
        """Get a program by program_code"""
        program = self.program_repo.get_by_code(program_code)
        
        if not program:
            return None
        
        return {
            'program_code': program['program_code'],
            'program_name': program['program_name'],
            'duration_years': program['duration_years']
        }
