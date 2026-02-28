#!/bin/bash

# Start TAFE Student Management API (Flask-only)
echo "=========================================="
echo "TAFE Student Management API v1"
echo "=========================================="

# Kill any existing Flask server on port 5001
echo "Checking for existing server on port 5001..."
if lsof -ti:5001 > /dev/null 2>&1; then
    echo "Killing existing server..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 1
    echo "✓ Existing server stopped"
else
    echo "✓ No existing server found"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Initialize database if it doesn't exist
if [ ! -f "students.db" ]; then
    echo "Initializing database..."
    python database.py
fi

# Start the Flask application
echo ""
echo "=========================================="
echo "Starting Flask Development Server..."
echo "=========================================="
echo "📊 API Documentation: http://localhost:5001/api/docs"
echo "💚 Health Check: http://localhost:5001/api/health"
echo "📚 Programs: http://localhost:5001/api/v1/programs"
echo "👥 Students: http://localhost:5001/api/v1/students"
echo ""
echo "🧪 Test with: python simple_rest_client.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python app.py
