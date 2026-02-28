#!/usr/bin/env python3
"""
Comprehensive endpoint test for TAFE Student Management API v1
Tests all endpoints to verify the API is working correctly
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5001"
API_V1 = f"{BASE_URL}/api/v1"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

test_results = []

def print_test(name, passed, details=""):
    """Print test result"""
    status = f"{GREEN}✓ PASS{RESET}" if passed else f"{RED}✗ FAIL{RESET}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")
    test_results.append((name, passed))

def test_health_check():
    """Test health check endpoint"""
    print(f"\n{BLUE}=== Testing Health Check ==={RESET}")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=10)
        passed = response.status_code == 200 and response.json().get('status') == 'healthy'
        print_test("Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Health Check", False, f"Error: {e}")
        return False

def test_get_programs():
    """Test GET /api/v1/programs"""
    print(f"\n{BLUE}=== Testing Programs Endpoints ==={RESET}")
    try:
        response = requests.get(f"{API_V1}/programs", timeout=10)
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get('success') == True and 
                 'data' in data and
                 len(data['data']) > 0)
        print_test("GET /api/v1/programs", passed, 
                  f"Status: {response.status_code}, Programs: {len(data.get('data', []))}")
        return data.get('data', []) if passed else []
    except Exception as e:
        print_test("GET /api/v1/programs", False, f"Error: {e}")
        return []

def test_get_program_by_id(program_id):
    """Test GET /api/v1/programs/{id}"""
    try:
        response = requests.get(f"{API_V1}/programs/{program_id}", timeout=10)
        data = response.json()
        passed = response.status_code == 200 and data.get('success') == True
        print_test(f"GET /api/v1/programs/{program_id}", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"GET /api/v1/programs/{program_id}", False, f"Error: {e}")
        return False

def test_get_students():
    """Test GET /api/v1/students with pagination"""
    print(f"\n{BLUE}=== Testing Students Endpoints ==={RESET}")
    try:
        response = requests.get(f"{API_V1}/students?page=1&per_page=5", timeout=10)
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get('success') == True and 
                 'pagination' in data and
                 'data' in data)
        print_test("GET /api/v1/students (paginated)", passed, 
                  f"Status: {response.status_code}, Total: {data.get('pagination', {}).get('total', 0)}")
        return data.get('data', []) if passed else []
    except Exception as e:
        print_test("GET /api/v1/students", False, f"Error: {e}")
        return []

def test_get_student_by_id(student_id):
    """Test GET /api/v1/students/{id}"""
    try:
        response = requests.get(f"{API_V1}/students/{student_id}", timeout=10)
        data = response.json()
        passed = response.status_code == 200 and data.get('success') == True
        print_test(f"GET /api/v1/students/{student_id}", passed, 
                  f"Status: {response.status_code}")
        return data.get('data') if passed else None
    except Exception as e:
        print_test(f"GET /api/v1/students/{student_id}", False, f"Error: {e}")
        return None

def test_create_student(program_id):
    """Test POST /api/v1/students"""
    try:
        new_student = {
            "first_name": "Test",
            "last_name": "Student",
            "email": f"test.student.{datetime.now().timestamp()}@student.tafe.edu.au",
            "program_id": program_id,
            "enrollment_date": datetime.now().strftime('%Y-%m-%d')
        }
        response = requests.post(f"{API_V1}/students", json=new_student, timeout=10)
        data = response.json()
        passed = response.status_code == 201 and data.get('success') == True
        student_id = data.get('data', {}).get('id') if passed else None
        print_test("POST /api/v1/students", passed, 
                  f"Status: {response.status_code}, ID: {student_id}")
        return student_id
    except Exception as e:
        print_test("POST /api/v1/students", False, f"Error: {e}")
        return None

def test_update_student(student_id):
    """Test PUT /api/v1/students/{id}"""
    try:
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        response = requests.put(f"{API_V1}/students/{student_id}", json=update_data, timeout=10)
        data = response.json()
        passed = response.status_code == 200 and data.get('success') == True
        print_test(f"PUT /api/v1/students/{student_id}", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"PUT /api/v1/students/{student_id}", False, f"Error: {e}")
        return False

def test_delete_student(student_id):
    """Test DELETE /api/v1/students/{id}"""
    try:
        response = requests.delete(f"{API_V1}/students/{student_id}", timeout=10)
        data = response.json()
        passed = response.status_code == 200 and data.get('success') == True
        print_test(f"DELETE /api/v1/students/{student_id}", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test(f"DELETE /api/v1/students/{student_id}", False, f"Error: {e}")
        return False

def test_404_error():
    """Test 404 error handling"""
    print(f"\n{BLUE}=== Testing Error Handling ==={RESET}")
    try:
        response = requests.get(f"{API_V1}/students/NOTEXIST999", timeout=10)
        passed = response.status_code == 404
        print_test("404 Error Handling", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("404 Error Handling", False, f"Error: {e}")
        return False

def test_validation_error():
    """Test validation error handling"""
    try:
        invalid_student = {
            "first_name": "Test"
            # Missing required fields
        }
        response = requests.post(f"{API_V1}/students", json=invalid_student, timeout=10)
        passed = response.status_code == 400
        print_test("400 Validation Error", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("400 Validation Error", False, f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}TAFE Student Management API v1 - Endpoint Tests{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    
    # Check if server is running
    if not test_health_check():
        print(f"\n{RED}❌ Server is not running! Start with: ./start.sh{RESET}")
        sys.exit(1)
    
    # Test Programs
    programs = test_get_programs()
    if programs:
        test_get_program_by_id(programs[0]['id'])
    
    # Test Students
    students = test_get_students()
    if students:
        test_get_student_by_id(students[0]['id'])
    
    # Test CRUD operations
    if programs:
        created_student_id = test_create_student(programs[0]['id'])
        if created_student_id:
            test_update_student(created_student_id)
            test_delete_student(created_student_id)
    
    # Test error handling
    test_404_error()
    test_validation_error()
    
    # Summary
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}Test Summary{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    
    passed = sum(1 for _, p in test_results if p)
    total = len(test_results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {GREEN}{passed}{RESET}")
    print(f"Failed: {RED}{total - passed}{RESET}")
    print(f"Success Rate: {GREEN if percentage == 100 else YELLOW}{percentage:.1f}%{RESET}")
    
    if percentage == 100:
        print(f"\n{GREEN}✅ All tests passed! API is ready for deployment.{RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}❌ Some tests failed. Please review the errors above.{RESET}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1)
