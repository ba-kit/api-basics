# REST API Principles

## What is REST?

**REST (Representational State Transfer)** is an architectural style for designing networked applications. A RESTful API follows specific principles that make it predictable, scalable, and easy to use.

REST was introduced by Roy Fielding in 2000 and has become the standard for web APIs.

## Core Principles of REST

### 1. Resource-Based Architecture

In REST, everything is a **resource**. A resource is any piece of information that can be named.

**Examples of Resources:**
- A student
- A collection of students
- A program
- A collection of programs

**Resources are identified by URLs:**
```
/api/students          → Collection of students
/api/students/1        → Specific student (ID: 1)
/api/programs          → Collection of programs
/api/programs/2        → Specific program (ID: 2)
```

### 2. Use Standard HTTP Methods

REST uses HTTP methods to perform operations on resources. This is called **CRUD** (Create, Read, Update, Delete).

| Operation | HTTP Method | Example | Description |
|-----------|-------------|---------|-------------|
| **Create** | POST | `POST /api/students` | Create a new student |
| **Read** | GET | `GET /api/students` | Get all students |
| **Read** | GET | `GET /api/students/1` | Get specific student |
| **Update** | PUT | `PUT /api/students/1` | Update student |
| **Delete** | DELETE | `DELETE /api/students/1` | Delete student |

### 3. Stateless Communication

Each request from client to server must contain all information needed to understand and process the request. The server doesn't store any client context between requests.

**Stateless Example:**
```http
GET /api/students/1 HTTP/1.1
Host: tafe-student-api.fly.dev
Accept: application/json
```

Every request is independent. The server doesn't remember previous requests.

### 4. Client-Server Separation

The client and server are independent. They can evolve separately as long as the API contract (interface) remains the same.

- **Client**: Handles user interface and user experience
- **Server**: Handles data storage, business logic, and data processing

### 5. Uniform Interface

REST APIs should have a consistent, predictable structure. This makes them easier to understand and use.

**Consistent URL patterns:**
```
GET    /api/students          → List all students
POST   /api/students          → Create a student
GET    /api/students/1        → Get student 1
PUT    /api/students/1        → Update student 1
DELETE /api/students/1        → Delete student 1
```

### 6. Representation of Resources

Resources can have multiple representations (JSON, XML, HTML). The most common format is **JSON**.

**JSON Representation of a Student:**
```json
{
  "id": 1,
  "first_name": "Emma",
  "last_name": "Smith",
  "email": "emma.smith@student.tafe.edu.au",
  "enrollment_date": "2024-02-15",
  "program": {
    "id": 2,
    "program_name": "Diploma of Software Development",
    "program_code": "ICT50220",
    "duration_years": 2
  }
}
```

## RESTful URL Design

### Good URL Patterns

✅ **Use nouns, not verbs**
```
Good: GET /api/students
Bad:  GET /api/getStudents
```

✅ **Use plural nouns for collections**
```
Good: GET /api/students
Bad:  GET /api/student
```

✅ **Use path parameters for specific resources**
```
Good: GET /api/students/1
Bad:  GET /api/students?id=1
```

✅ **Use query parameters for filtering, sorting, pagination**
```
Good: GET /api/students?program_id=2&page=1&per_page=10
```

✅ **Use hierarchical structure for relationships**
```
Good: GET /api/programs/2/students
```

✅ **Keep URLs lowercase and use hyphens for readability**
```
Good: GET /api/student-records
Bad:  GET /api/StudentRecords
Bad:  GET /api/student_records
```

### URL Examples from Our API

```
GET    /api/health                    → Health check
GET    /api/programs                  → List all programs
GET    /api/programs/1                → Get program 1
GET    /api/students                  → List all students
GET    /api/students?program_id=2     → Filter students by program
GET    /api/students?page=2           → Get page 2 of students
GET    /api/students/1                → Get student 1
POST   /api/students                  → Create new student
PUT    /api/students/1                → Update student 1
DELETE /api/students/1                → Delete student 1
```

## HTTP Status Codes in REST

RESTful APIs use HTTP status codes to indicate the result of operations.

### Success Responses

| Code | When to Use | Example |
|------|-------------|---------|
| **200 OK** | Successful GET, PUT, DELETE | `GET /api/students/1` |
| **201 Created** | Successful POST (resource created) | `POST /api/students` |
| **204 No Content** | Successful DELETE (no content to return) | `DELETE /api/students/1` |

### Client Error Responses

| Code | When to Use | Example |
|------|-------------|---------|
| **400 Bad Request** | Invalid request format or validation error | Missing required fields |
| **404 Not Found** | Resource doesn't exist | `GET /api/students/9999` |
| **409 Conflict** | Request conflicts with current state | Duplicate email address |

### Server Error Responses

| Code | When to Use | Example |
|------|-------------|---------|
| **500 Internal Server Error** | Unexpected server error | Database connection failed |

## Request and Response Format

### Standard Response Structure

Our API uses a consistent response format:

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "Emma",
    "last_name": "Smith"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Student not found"
}
```

**List Response with Pagination:**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 20,
    "page": 1,
    "per_page": 10,
    "total_pages": 2
  }
}
```

## REST API Best Practices

### 1. Use Proper HTTP Methods

Match the HTTP method to the operation:
- **GET**: Read data (safe, idempotent)
- **POST**: Create new resources
- **PUT**: Update existing resources (idempotent)
- **DELETE**: Remove resources (idempotent)

### 2. Return Appropriate Status Codes

Don't return `200 OK` for everything. Use the right status code:
- `201` when creating resources
- `404` when resources aren't found
- `400` for validation errors
- `500` for server errors

### 3. Use JSON for Data Exchange

JSON is the standard format for REST APIs:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@student.tafe.edu.au"
}
```

### 4. Implement Filtering, Sorting, and Pagination

For large datasets, provide ways to filter and paginate:
```
GET /api/students?program_id=2&page=1&per_page=10
```

### 5. Version Your API

Include version in the URL to allow for future changes:
```
/api/v1/students
/api/v2/students
```

### 6. Provide Clear Error Messages

Help developers understand what went wrong:
```json
{
  "success": false,
  "error": "Validation failed",
  "details": [
    "first_name is required",
    "email must be valid"
  ]
}
```

### 7. Use Nested Resources for Relationships

Show relationships in the response:
```json
{
  "id": 1,
  "first_name": "Emma",
  "last_name": "Smith",
  "program": {
    "id": 2,
    "program_name": "Diploma of Software Development"
  }
}
```

## CRUD Operations Example

Let's see how CRUD operations work with our Student resource:

### Create (POST)

**Request:**
```http
POST /api/students HTTP/1.1
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@student.tafe.edu.au",
  "program_id": 2
}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 21,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@student.tafe.edu.au",
    "enrollment_date": "2024-02-26",
    "program_id": 2
  }
}
```

### Read (GET)

**Request:**
```http
GET /api/students/21 HTTP/1.1
Accept: application/json
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 21,
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john.doe@student.tafe.edu.au",
    "enrollment_date": "2024-02-26",
    "program": {
      "id": 2,
      "program_name": "Diploma of Software Development",
      "program_code": "ICT50220",
      "duration_years": 2
    }
  }
}
```

### Update (PUT)

**Request:**
```http
PUT /api/students/21 HTTP/1.1
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@student.tafe.edu.au",
  "program_id": 3
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Student updated successfully",
  "data": {
    "id": 21,
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@student.tafe.edu.au",
    "enrollment_date": "2024-02-26",
    "program_id": 3
  }
}
```

### Delete (DELETE)

**Request:**
```http
DELETE /api/students/21 HTTP/1.1
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Student deleted successfully"
}
```

## Idempotency

An operation is **idempotent** if performing it multiple times has the same effect as performing it once.

| Method | Idempotent? | Explanation |
|--------|-------------|-------------|
| GET | ✅ Yes | Reading data doesn't change it |
| POST | ❌ No | Each request creates a new resource |
| PUT | ✅ Yes | Updating to the same values multiple times has the same effect |
| DELETE | ✅ Yes | Deleting the same resource multiple times has the same effect |

## API Versioning

As your API evolves, you may need to make breaking changes. Versioning allows old clients to continue working while new clients use new features.

**Common versioning strategies:**

1. **URL Path Versioning** (Recommended)
```
/api/v1/students
/api/v2/students
```

2. **Query Parameter Versioning**
```
/api/students?version=1
```

3. **Header Versioning**
```
Accept: application/vnd.tafe.v1+json
```

## Common Mistakes to Avoid

❌ **Using verbs in URLs**
```
Bad:  POST /api/createStudent
Good: POST /api/students
```

❌ **Returning wrong status codes**
```
Bad:  Return 200 for all responses
Good: Return 201 for created, 404 for not found, etc.
```

❌ **Inconsistent naming**
```
Bad:  /api/students, /api/Program, /api/course_list
Good: /api/students, /api/programs, /api/courses
```

❌ **Not handling errors properly**
```
Bad:  Return HTML error page
Good: Return JSON error with proper status code
```

❌ **Making APIs stateful**
```
Bad:  Storing session data on server
Good: Each request contains all needed information
```

## Key Takeaways

1. **Resources are nouns**: Use `/api/students`, not `/api/getStudents`
2. **HTTP methods are verbs**: GET, POST, PUT, DELETE
3. **Status codes matter**: Use the right code for each situation
4. **Be consistent**: Follow the same patterns throughout your API
5. **Think in resources**: Design around data entities, not actions
6. **Use JSON**: It's the standard format for modern APIs
7. **Document your API**: Use tools like Swagger for documentation

## Next Steps

Now that you understand REST principles:
1. Explore the [HTTP Basics Guide](http_basics.md) for more details on HTTP
2. Try the API using Postman with the provided collection
3. Review the Swagger documentation at `https://tafe-student-api.fly.dev/api/docs`
4. Experiment with creating, reading, updating, and deleting students
