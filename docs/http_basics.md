# HTTP Basics Guide

## What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. It's a protocol that defines how messages are formatted and transmitted between clients (like web browsers or Postman) and servers (like our Flask API).

## HTTP Request-Response Cycle

Every API interaction follows a simple pattern:

1. **Client** sends an HTTP **Request** to the server
2. **Server** processes the request
3. **Server** sends back an HTTP **Response** to the client

```
Client (Postman)  ----[HTTP Request]---->  Server (Flask API)
                                            - Process request
                                            - Query database
                                            - Prepare response
Client (Postman)  <---[HTTP Response]----  Server (Flask API)
```

## HTTP Request Structure

An HTTP request consists of three main parts:

### 1. Request Line
Contains the HTTP method, URL path, and HTTP version.

```
GET /api/students/1 HTTP/1.1
```

### 2. Headers
Metadata about the request (key-value pairs).

```
Host: localhost:5000
Content-Type: application/json
Accept: application/json
User-Agent: PostmanRuntime/7.32.0
```

**Common Headers:**
- `Content-Type`: Format of the data being sent (e.g., `application/json`)
- `Accept`: Format the client expects in response (e.g., `application/json`)
- `Authorization`: Credentials for authentication (not used in this demo)
- `User-Agent`: Information about the client making the request

### 3. Body (Optional)
The actual data being sent (only for POST, PUT, PATCH requests).

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@student.tafe.edu.au",
  "program_id": 2
}
```

## HTTP Response Structure

An HTTP response also has three main parts:

### 1. Status Line
Contains HTTP version, status code, and status message.

```
HTTP/1.1 200 OK
```

### 2. Headers
Metadata about the response.

```
Content-Type: application/json
Content-Length: 245
Date: Mon, 26 Feb 2024 12:00:00 GMT
Server: Werkzeug/3.0.1 Python/3.11.0
```

### 3. Body
The actual data returned by the server.

```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "Emma",
    "last_name": "Smith",
    "email": "emma.smith@student.tafe.edu.au"
  }
}
```

## HTTP Methods (Verbs)

HTTP methods indicate the desired action to be performed on a resource.

### GET - Retrieve Data
- **Purpose**: Fetch data from the server
- **Has Body**: No
- **Idempotent**: Yes (multiple identical requests have the same effect)
- **Example**: Get list of students

```http
GET /api/students HTTP/1.1
Host: localhost:5000
Accept: application/json
```

### POST - Create New Resource
- **Purpose**: Create a new resource on the server
- **Has Body**: Yes
- **Idempotent**: No (each request creates a new resource)
- **Example**: Create a new student

```http
POST /api/students HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@student.tafe.edu.au",
  "program_id": 2
}
```

### PUT - Update Existing Resource
- **Purpose**: Update an entire resource
- **Has Body**: Yes
- **Idempotent**: Yes (multiple identical updates have the same effect)
- **Example**: Update student information

```http
PUT /api/students/1 HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@student.tafe.edu.au",
  "program_id": 3
}
```

### DELETE - Remove Resource
- **Purpose**: Delete a resource from the server
- **Has Body**: No
- **Idempotent**: Yes (deleting the same resource multiple times has the same effect)
- **Example**: Delete a student

```http
DELETE /api/students/1 HTTP/1.1
Host: localhost:5000
```

### Other Methods (Not Used in This Demo)
- **PATCH**: Partially update a resource (only specific fields)
- **HEAD**: Same as GET but only returns headers (no body)
- **OPTIONS**: Get information about allowed methods for a resource

## HTTP Status Codes

Status codes indicate the result of the HTTP request. They are grouped into five categories:

### 1xx - Informational
Request received, continuing process (rarely used in REST APIs).

### 2xx - Success
The request was successfully received, understood, and accepted.

| Code | Message | Meaning | Example |
|------|---------|---------|---------|
| **200** | OK | Request succeeded | GET /api/students |
| **201** | Created | New resource created | POST /api/students |
| **204** | No Content | Success but no content to return | DELETE /api/students/1 |

### 3xx - Redirection
Further action needed to complete the request (rarely used in REST APIs).

### 4xx - Client Errors
The request contains bad syntax or cannot be fulfilled due to client error.

| Code | Message | Meaning | Example |
|------|---------|---------|---------|
| **400** | Bad Request | Invalid request format or validation error | Missing required fields |
| **401** | Unauthorized | Authentication required | Missing or invalid credentials |
| **403** | Forbidden | Client doesn't have permission | Insufficient privileges |
| **404** | Not Found | Resource doesn't exist | GET /api/students/9999 |
| **409** | Conflict | Request conflicts with current state | Email already exists |

### 5xx - Server Errors
The server failed to fulfill a valid request.

| Code | Message | Meaning | Example |
|------|---------|---------|---------|
| **500** | Internal Server Error | Unexpected server error | Database connection failed |
| **503** | Service Unavailable | Server temporarily unavailable | Server maintenance |

## Content Negotiation

Content negotiation allows clients and servers to agree on the format of data being exchanged.

### Content-Type Header
Tells the server what format the request body is in.

```
Content-Type: application/json
```

**Common values:**
- `application/json` - JSON data
- `application/xml` - XML data
- `text/html` - HTML content
- `multipart/form-data` - File uploads

### Accept Header
Tells the server what format the client wants in the response.

```
Accept: application/json
```

## Practical Examples

### Example 1: GET Request (Retrieve Student)

**Request:**
```http
GET /api/students/1 HTTP/1.1
Host: localhost:5000
Accept: application/json
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 312

{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "Emma",
    "last_name": "Smith",
    "full_name": "Emma Smith",
    "email": "emma.smith@student.tafe.edu.au",
    "enrollment_date": "2024-02-15",
    "program": {
      "id": 2,
      "program_name": "Diploma of Software Development",
      "program_code": "ICT50220",
      "duration_years": 2
    }
  }
}
```

### Example 2: POST Request (Create Student)

**Request:**
```http
POST /api/students HTTP/1.1
Host: localhost:5000
Content-Type: application/json
Accept: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@student.tafe.edu.au",
  "enrollment_date": "2024-02-26",
  "program_id": 2
}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 198

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

### Example 3: Error Response (404 Not Found)

**Request:**
```http
GET /api/students/9999 HTTP/1.1
Host: localhost:5000
Accept: application/json
```

**Response:**
```http
HTTP/1.1 404 Not Found
Content-Type: application/json
Content-Length: 58

{
  "success": false,
  "error": "Student not found"
}
```

## Testing with Postman

### Viewing Request Details in Postman

1. **Method Dropdown**: Select GET, POST, PUT, DELETE
2. **URL Bar**: Enter the endpoint URL
3. **Headers Tab**: View and modify request headers
4. **Body Tab**: Add request body (for POST/PUT)
5. **Send Button**: Execute the request

### Viewing Response Details in Postman

1. **Status**: Shows status code (200, 404, etc.)
2. **Time**: Request duration
3. **Size**: Response size
4. **Body Tab**: View response data
5. **Headers Tab**: View response headers

## Key Takeaways

1. **HTTP is stateless**: Each request is independent; the server doesn't remember previous requests
2. **Methods have meaning**: Use GET for reading, POST for creating, PUT for updating, DELETE for removing
3. **Status codes matter**: They tell you if the request succeeded and why it might have failed
4. **Headers provide context**: They describe the data format and other metadata
5. **JSON is the standard**: Most modern APIs use JSON for data exchange

## Next Steps

Now that you understand HTTP basics, learn about [REST API Principles](rest_principles.md) to understand how to design well-structured APIs.
