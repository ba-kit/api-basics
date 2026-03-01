# TAFE Student Management API v1

A REST API training project for teaching API integration basics to Business Analysts. Demonstrates HTTP fundamentals, RESTful design, layered architecture, and API testing.

## �️ Project Structure

```
SIMS/
├── app.py                    # Flask routes (API v1)
├── database.py               # SQLite schema and seed data
├── start.sh                  # Start server (auto-kills existing)
├── requirements.txt          # Dependencies (Flask, CORS, Swagger UI)
├── requirements-dev.txt      # Dev dependencies (+ requests)
├── swagger.yaml              # OpenAPI v1 specification
├── test_all_endpoints.py     # Automated endpoint tests
├── simple_rest_client.py     # Demo REST client for KT sessions
├── Dockerfile                # Container build
├── fly.toml                  # Fly.io deployment config
├── services/
│   ├── student_service.py    # Student business logic
│   └── program_service.py    # Program business logic
├── repositories/
│   ├── base_repository.py    # Shared DB operations
│   ├── student_repository.py # Student data access
│   └── program_repository.py # Program data access
├── docs/
│   ├── index.md              # KT session document (GitHub Pages)
│   ├── http_basics.md        # HTTP fundamentals guide
│   ├── rest_principles.md    # REST principles guide
│   └── _config.yml           # Jekyll theme config
└── postman/
    └── TAFE_Student_API.postman_collection.json
```

## 🚀 Quick Start

```bash
# Start server (creates venv, installs deps, kills existing server)
./start.sh
```

Or manually:

```bash
source venv/bin/activate
python database.py    # only needed first time or to reset
python app.py
```

- **Health Check**: http://localhost:5001/api/health
- **Swagger UI**: http://localhost:5001/api/docs

## 📖 API Endpoints (v1)

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |

### Programs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/programs` | List all programs |
| GET | `/api/v1/programs/{id}` | Get program by ID |

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/students` | List students (paginated) |
| GET | `/api/v1/students/{id}` | Get student details (nested JSON) |
| POST | `/api/v1/students` | Create new student |
| PUT | `/api/v1/students/{id}` | Update student |
| DELETE | `/api/v1/students/{id}` | Delete student |

**Pagination:** `GET /api/v1/students?page=1&per_page=10`

## 📊 Response Format

```json
{ "success": true, "data": { ... } }
{ "success": false, "error": "message" }
{ "success": true, "data": [...], "pagination": { "total": 20, "page": 1, "per_page": 10, "total_pages": 2 } }
```

## 🧪 Testing

```bash
# Automated tests (server must be running)
source venv/bin/activate && python test_all_endpoints.py

# Demo REST client for KT sessions
source venv/bin/activate && python simple_rest_client.py
```

## 📦 Postman Collection

Import `postman/TAFE_Student_API.postman_collection.json` into Postman.
The collection variable `base_url` is set to `http://localhost:5001`.

## 🗄️ Database

```bash
# Reset with fresh seed data (10 programs, 20 students)
source venv/bin/activate && python database.py

# Inspect via SQLite CLI
sqlite3 students.db "SELECT s.id, s.first_name, p.program_code FROM students s JOIN programs p ON s.program_id = p.id LIMIT 5;"
```

Student IDs use the format `ACT001`, `ACT002`, etc.

## 🛠️ HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Validation error |
| 404 | Not found |
| 409 | Duplicate email |
| 500 | Server error |

## 🐳 Fly.io Deployment

```bash
fly auth login
fly volumes create data --size 1
fly deploy
fly logs
```

## 🔍 Troubleshooting

| Problem | Fix |
|---------|-----|
| Port 5001 in use | `./start.sh` kills existing process automatically |
| Server hangs | Already fixed: `debug=False, use_reloader=False` |
| Database locked | Close any SQLite browsers and restart |
| Import errors | `source venv/bin/activate && pip install -r requirements.txt` |
| SSH permission denied | `ssh-add ~/.ssh/id_ed25519_tafe` |

---

Built for TAFE BA Team Training 🎓
