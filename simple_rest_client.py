#!/usr/bin/env python3
"""
Simple REST Client for TAFE Student Management API
A basic client to demonstrate API operations before introducing Postman
"""

import requests
import json
from datetime import datetime

# Configuration
# Production URL (change to http://localhost:5001 for local development)
BASE_URL = "https://tafe-student-api.fly.dev"
API_BASE = f"{BASE_URL}/api/v1"

def print_response(response, operation):
    """Print formatted response for team demonstration"""
    print(f"\n{'='*50}")
    print(f"Operation: {operation}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"{'='*50}\n")

def health_check():
    """Check if API is running"""
    print("🔍 Checking API Health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print_response(response, "Health Check")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to API: {e}")
        return False

def get_all_students():
    """Get all students"""
    print("📚 Getting All Students...")
    try:
        response = requests.get(f"{API_BASE}/students")
        print_response(response, "GET All Students")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def get_student(student_id):
    """Get a specific student"""
    print(f"👤 Getting Student {student_id}...")
    try:
        response = requests.get(f"{API_BASE}/students/{student_id}")
        print_response(response, f"GET Student {student_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def create_student():
    """Create a new student"""
    print("➕ Creating New Student...")
    new_student = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@student.tafe.edu.au",
        "program_id": 2
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/students",
            json=new_student,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "CREATE Student")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def update_student(student_id):
    """Update a student"""
    print(f"✏️ Updating Student {student_id}...")
    update_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@student.tafe.edu.au"
    }
    
    try:
        response = requests.put(
            f"{API_BASE}/students/{student_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print_response(response, f"UPDATE Student {student_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def delete_student(student_id):
    """Delete a student"""
    print(f"🗑️ Deleting Student {student_id}...")
    try:
        response = requests.delete(f"{API_BASE}/students/{student_id}")
        print_response(response, f"DELETE Student {student_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def get_programs():
    """Get all programs"""
    print("📖 Getting All Programs...")
    try:
        response = requests.get(f"{API_BASE}/programs")
        print_response(response, "GET All Programs")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None

def demonstrate_errors():
    """Demonstrate common error scenarios"""
    print("\n🚨 Demonstrating Error Scenarios...")
    
    # 404 Error - Student not found
    print("\n1. Testing 404 Error (Student Not Found):")
    get_student("ACT999")
    
    # 400 Error - Invalid data
    print("\n2. Testing 400 Error (Invalid Data):")
    try:
        response = requests.post(
            f"{API_BASE}/students",
            json={"invalid": "data"},
            headers={"Content-Type": "application/json"}
        )
        print_response(response, "POST Invalid Data")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

def main():
    """Main demonstration function"""
    print("🚀 TAFE Student Management API - Simple REST Client")
    print("=" * 60)
    print("This client demonstrates basic API operations")
    print("Use this to explain REST concepts before introducing Postman")
    print("=" * 60)
    
    # Check if API is running
    if not health_check():
        print("❌ API is not running. Please start the API server first.")
        print("💡 Run: python app.py")
        return
    
    # Demonstrate CRUD operations
    print("\n📋 CRUD Operations Demonstration:")
    
    # 1. Get all programs first
    get_programs()
    
    # 2. Get all students
    get_all_students()
    
    # 3. Get a specific student
    get_student("ACT001")
    
    # 4. Create a new student
    result = create_student()
    if result and result.get('success'):
        new_student_id = result['data']['id']
        print(f"✅ Created student with ID: {new_student_id}")
        
        # 5. Get the new student
        get_student(new_student_id)
        
        # 6. Update the new student
        update_student(new_student_id)
        
        # 7. Delete the new student
        delete_student(new_student_id)
    
    # 8. Demonstrate errors
    demonstrate_errors()
    
    print("\n✅ Demonstration Complete!")
    print("💡 Key Points to Explain:")
    print("   • HTTP Methods: GET, POST, PUT, DELETE")
    print("   • Status Codes: 200 (success), 201 (created), 400 (bad request), 404 (not found)")
    print("   • Request/Response Format: JSON")
    print("   • Student IDs: String format (ACT001, ACT002, etc.)")
    print("   • API Endpoints: /api/students, /api/programs")

if __name__ == "__main__":
    main()
