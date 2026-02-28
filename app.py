from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Lazy initialization of services to avoid import-time database connections
_student_service = None
_program_service = None

def get_student_service():
    global _student_service
    if _student_service is None:
        from services.student_service import StudentService
        _student_service = StudentService()
    return _student_service

def get_program_service():
    global _program_service
    if _program_service is None:
        from services.program_service import ProgramService
        _program_service = ProgramService()
    return _program_service

# Swagger UI setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TAFE Student Management API v1"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/swagger.yaml')
def swagger_yaml():
    with open('swagger.yaml', 'r') as f:
        content = f.read()
    return app.response_class(content, mimetype='text/yaml')

# Create v1 API blueprint
v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

# Health check endpoint (no versioning)
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'TAFE Student Management API',
        'version': 'v1'
    }), 200

# Programs endpoints
@v1_bp.route('/programs', methods=['GET'])
def get_programs():
    try:
        programs = get_program_service().get_all_programs()
        
        return jsonify({
            'success': True,
            'data': programs
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@v1_bp.route('/programs/<int:program_id>', methods=['GET'])
def get_program(program_id):
    try:
        program = get_program_service().get_program_by_id(program_id)
        
        if not program:
            return jsonify({
                'success': False,
                'error': 'Program not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': program
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Students endpoints
@v1_bp.route('/students', methods=['GET'])
def get_students():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        result = get_student_service().get_all_students(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result['items'],
            'pagination': {
                'total': result['total'],
                'page': result['page'],
                'per_page': result['per_page'],
                'total_pages': result['total_pages']
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@v1_bp.route('/students/<string:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        student = get_student_service().get_student_by_id(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': student
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@v1_bp.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        errors = get_student_service().validate_student_data(data)
        if errors:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': errors
            }), 400
        
        student = get_student_service().create_student(
            data['first_name'],
            data['last_name'],
            data['email'],
            data['program_id'],
            data.get('enrollment_date')
        )
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'data': student
        }), 201
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@v1_bp.route('/students/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must be JSON'
            }), 400
        
        student = get_student_service().update_student(
            student_id,
            data.get('first_name'),
            data.get('last_name'),
            data.get('email'),
            data.get('enrollment_date'),
            data.get('program_id')
        )
        
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully',
            'data': student
        }), 200
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@v1_bp.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        success = get_student_service().delete_student(student_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Student deleted successfully'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Register v1 blueprint
app.register_blueprint(v1_bp)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    
    print("🚀 Starting TAFE Student Management API v1...")
    print(f"📊 API Documentation: http://localhost:{port}/api/docs")
    print(f"💚 Health Check: http://localhost:{port}/api/health")
    print(f"📚 Programs: http://localhost:{port}/api/v1/programs")
    print(f"👥 Students: http://localhost:{port}/api/v1/students")
    print("")
    print("✅ Fast startup with lazy initialization!")
    
    # Disable reloader to avoid macOS issues - use debug=False, use_reloader=False
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
