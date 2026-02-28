FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Initialize database on build
RUN python database.py

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
