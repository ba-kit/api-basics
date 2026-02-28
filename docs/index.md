# API Integration Guide for Business Analysts

**Welcome to your API training session!** This guide will help you understand how APIs work from a business perspective, enabling you to write better requirements and communicate more effectively with technical teams.

## What You'll Learn

By the end of this session, you will be able to:
- Understand how APIs work without needing to code
- Read Swagger documentation and extract business requirements
- Use Postman to test APIs and validate requirements
- Write clear, precise API requirements that developers can implement
- Identify data transformation requirements from API responses

## Getting Started

### Setup Your Environment

1. **Open your browser to:** http://localhost:5001/api/docs (our API documentation)
2. **Start the API server:** `python app.py`
3. **Try the simple REST client:** `python simple_rest_client.py`
4. **Download Postman** if not already installed: https://www.postman.com/downloads/
5. **Import the Postman collection:** `postman/TAFE_Student_API.postman_collection.json`

### Simple REST Client

Before using Postman, try our simple Python client to understand the basics:

```bash
python simple_rest_client.py
```

This demonstrates:
- All CRUD operations (Create, Read, Update, Delete)
- Error handling (404, 400 errors)
- Request/response format
- Student ID format (ACT001, ACT002)

**Use this client to explain REST concepts to your team before introducing Postman!**

### Our Training API

We'll be working with a **TAFE Student Management API** that manages:
- Students enrolled in programs
- Program information and enrollment counts
- Complete CRUD operations for student records

This real API will help you understand concepts through hands-on examples.

### Database Structure

Our API uses a simple SQLite database with two main tables:

```
┌─────────────────────────────────────────────────────────────────┐
│                        TAFE Student Database                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐         ┌─────────────────────────────────┐ │
│  │    programs     │         │           students               │ │
│  ├─────────────────┤         ├─────────────────────────────────┤ │
│  │ id (INTEGER)    │◄─────────┤ program_id (INTEGER)            │ │
│  │ program_name    │         │ id (TEXT) - ACT001, ACT002...   │ │
│  │ program_code    │         │ first_name                      │ │
│  │ duration_years  │         │ last_name                       │ │
│  └─────────────────┘         │ email                           │ │
│                              │ enrollment_date                 │ │
│                              └─────────────────────────────────┘ │
│                                                                 │
│  Relationship: Many students belong to one program              │
│  Student IDs: String format (ACT001, ACT002, etc.)              │
└─────────────────────────────────────────────────────────────────┘
```

**Key Points:**
- Each student has a unique ID like "ACT001", "ACT002"
- Students belong to exactly one program
- Programs can have many students
- All data is stored in a single SQLite database file

---

## Understanding How APIs Work

### The Request-Response Cycle

Every API interaction follows this simple pattern:

```
You (in Postman)  ----[Request]---->  Server (API)
                                      - Processes your request
                                      - Gets data from database
                                      - Sends response back
You (in Postman)  <---[Response]----  Server (API)
```

### What Happens When You Make an API Call

**Example: Getting Student Details**
```http
GET /api/students/1 HTTP/1.1
Host: localhost:5001
Accept: application/json
```

**In plain English:** "Show me the student with ID 1, and give me the data in JSON format."

### The Four Main API Operations

| Operation | What It Does | Business Example |
|-----------|--------------|------------------|
| **GET** | Read/Retrieve data | "Show me student details" |
| **POST** | Create new data | "Add a new student" |
| **PUT** | Update existing data | "Update student information" |
| **DELETE** | Remove data | "Delete a student record" |

### Understanding API Responses

**Success Responses (2xx):**
- `200 OK` = Your request worked perfectly
- `201 Created` = New record was successfully created

**Error Responses (4xx):**
- `400 Bad Request` = You sent invalid or incomplete data
- `404 Not Found` = The record you're looking for doesn't exist
- `409 Conflict` = You tried to create something that already exists

**Server Errors (5xx):**
- `500 Internal Server Error` = Something broke on the server side

### Why REST is Better for Business

**Modern APIs (REST) use clean JSON:**
```json
{
  "id": 1,
  "first_name": "Emma",
  "last_name": "Smith"
}
```

**Old APIs (SOAP) used complex XML:**
```xml
<soap:Envelope>
  <soap:Body>
    <GetStudentResponse>
      <Student>
        <id>1</id>
        <first_name>Emma</first_name>
        <last_name>Smith</last_name>
      </Student>
    </GetStudentResponse>
  </soap:Body>
</soap:Envelope>
```

**Result:** REST is much easier to read and understand for business users.

---

## Working with API URLs and Data

### Understanding API URLs

**Getting Collections vs. Individual Items:**
```
/api/students          → All students (list)
/api/students/1        → One specific student (ID 1)
/api/programs          → All programs
/api/programs/2        → One specific program (ID 2)
```

### Two Types of Parameters

**Path Parameters (to get a specific item):**
```
GET /api/students/1
```
*Translation: "Get me student #1"*

**Query Parameters (to filter, sort, or page through lists):**
```
GET /api/students?program_id=2&page=1&per_page=10
```
*Translation: "Get students from program 2, show page 1, 10 students per page"*

### Understanding Nested Data

**Real Example from Our Student API:**
```json
{
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
```

### Finding Data in Nested Structures

**Business Requirement:** "Display the program name on the student profile screen"

**API Field Location:** `program.program_name`

**Why This Matters:** The nested structure shows exactly where each piece of data lives. This prevents the common confusion that causes development delays.

### Working with Lists of Data

**Program with All Its Students:**
```json
{
  "id": 2,
  "program_name": "Diploma of Software Development",
  "enrolled_students": [
    {
      "id": 1,
      "first_name": "Emma",
      "last_name": "Smith",
      "email": "emma.smith@student.tafe.edu.au"
    },
    {
      "id": 3,
      "first_name": "James",
      "last_name": "Wilson",
      "email": "james.wilson@student.tafe.edu.au"
    }
  ]
}
```

**Questions to Ask When Writing Requirements:**
- Which student fields do we need to display?
- What order should they appear in?
- What happens if there are no students?
- How many students should show on each page?

---

## Reading API Documentation (Swagger)

### What is Swagger?

Swagger is an interactive documentation tool that shows you exactly how an API works. Think of it as a user manual for APIs.

**Open our API documentation:** http://localhost:5001/api/docs

### Understanding What You See

**1. API Endpoints:**
```
GET /api/students/{id}
```
- **GET** = What operation you can perform
- **/api/students/{id}** = Where to find the data
- **{id}** = You need to provide a student ID

**2. Request Information:**
- **Path Parameters:** Required information (like student ID)
- **Query Parameters:** Optional filters (like program ID)
- **Request Body:** Data you send when creating/updating

**3. Response Information:**
- **200 Response:** What you get when it works
- **400 Response:** What you get when you send bad data
- **404 Response:** What you get when something doesn't exist

### How to Extract Business Requirements

**What Swagger Shows → What It Means for Business:**

| Swagger Element | Business Translation | What You Need to Document |
|-----------------|---------------------|---------------------------|
| **Required fields** | Must-have information | Add to acceptance criteria |
| **Optional fields** | Nice-to-have information | Specify when to include |
| **Data types** | Format requirements | Text, numbers, dates, etc. |
| **Enum values** | Dropdown options | List all valid choices |
| **Nullable fields** | Can be empty | Plan empty state behavior |
| **Error responses** | Error handling | Document error messages |
| **Validation rules** | Data quality rules | Field-level validation |

### Real Example: Creating a Student

**What Swagger Tells Us:**
```yaml
required:
  - first_name
  - last_name  
  - email
  - program_id
properties:
  first_name:
    type: string
    example: John
  email:
    type: string
    format: email
    example: john.doe@student.tafe.edu.au
  program_id:
    type: integer
    example: 2
```

**Business Requirements You Should Write:**
- "First name is required and must be text"
- "Email is required and must be a valid email format"
- "Program must be selected from existing programs"
- "All fields must be validated before submission"
- "Show specific error messages for each invalid field"

---

## Testing APIs with Postman

### What is Postman?

Postman is a tool that lets you test APIs without writing any code. It's like a web browser specifically for APIs.

### Your First API Test

**Getting Student Details:**
1. Open Postman
2. Select "GET Student Details" from our collection
3. Click "Send"
4. Look at the response:
   - **Status:** 200 OK (it worked!)
   - **Body:** Student data with program information

**Creating a New Student:**
1. Select "Create New Student"
2. Click "Send"
3. Check the response:
   - **Status:** 201 Created (new student added)
   - **Body:** The new student's data with their ID

### Working with Different Environments

**Environment Variables** help you switch between different servers:
- **Development:** `http://localhost:5001` (our training server)
- **Testing:** `http://test-api.company.com` (company test server)
- **Production:** `http://api.company.com` (live server)

**How it works:** Change the `base_url` variable and all your requests automatically use the new server.

### Try These Exercises

**Exercise 1: Find Specific Information**
1. Get student with ID 5
2. Find their program name
3. Locate their enrollment date
4. Note any fields that are empty or missing

**Exercise 2: See Error Handling**
1. Try to create a student without a first name
2. Look at the 400 Bad Request response
3. Read the specific error messages
4. Fix the error and try again

**Exercise 3: Filter and Paginate**
1. Get all students in program 2
2. Use: `?program_id=2`
3. Count how many results you get
4. Try pagination: `?page=1&per_page=5`

### What You'll Learn

- **Real data vs. assumptions:** See actual API responses
- **Specific error messages:** Not just "it failed"
- **Data structure:** How fields are named and organized
- **Validation in action:** Rules are automatically enforced

---

## Understanding Data Transformations

### What Are Data Transformations?

Sometimes the data from an API needs to be changed before it can be displayed to users. These are called "transformations" and they need to be documented in your requirements.

### Three Common Transformation Scenarios

**Scenario 1: Creating Full Names**
```json
// What the API gives you:
{
  "first_name": "Emma",
  "last_name": "Smith"
}

// What users should see:
"Emma Smith"
```

**Your Requirement:** "Display full name by combining first_name and last_name fields"

---

**Scenario 2: Formatting Dates**
```json
// What the API gives you:
{
  "enrollment_date": "2024-02-15"
}

// What users should see:
"15 Feb 2024"
```

**Your Requirement:** "Display enrollment_date in 'DD MMM YYYY' format"

---

**Scenario 3: Filtering Data**
```json
// What the API gives you (all students):
[
  {"id": 1, "program_id": 2, "first_name": "Emma"},
  {"id": 2, "program_id": 3, "first_name": "John"},
  {"id": 3, "program_id": 2, "first_name": "James"}
]

// What users should see (only Program 2):
Emma Smith, James Wilson
```

**Your Requirement:** "Filter students to show only those in Program 2"

### Writing Better Requirements

**Instead of this vague requirement:**
> "Display student details"

**Write this detailed requirement:**
> **Endpoint:** GET /api/students/{id}
> **Method:** GET
> **Fields to Display:**
> - Full Name (combine first_name + last_name)
> - Email (use email field directly)
> - Program Name (use program.program_name from nested data)
> - Enrollment Date (format enrollment_date as "DD MMM YYYY")
> **Empty State:** If student not found, show "Student information unavailable"
> **Error Handling:** 
> - 404: Display "Student not found" message
> - 500: Display "System temporarily unavailable" message

### Requirements Template

Use this template for all API features:

```
**Feature:** [Name of the feature]
**Endpoint:** [HTTP Method + URL]
**Request Parameters:**
- [Parameter name]: [Type], Required/Optional, Description
**Response Fields:**
- [Display field]: [API source field], [Transformation rules]
**Business Rules:**
- [Rule 1]
- [Rule 2]
**Error Handling:**
- [Status code]: [Message to show user]
**Edge Cases:**
- [Situation]: [What should happen]
```

---

## Frequently Asked Questions

**Q: What if the API documentation is wrong or outdated?**
**A:** Document what you find that's different, tell the development team, and treat it as a project risk. Always test your assumptions with real API calls.

**Q: Who should raise concerns about API design?**
**A:** Everyone! As a BA, you're in a unique position to spot usability issues that developers might miss. If an API doesn't support what the business needs, speak up early.

**Q: How do I write requirements for an API that doesn't exist yet?**
**A:** Start with what the business needs, then work backwards to figure out what the API should look like. Create example responses to test your thinking before development starts.

**Q: Do I need to learn how to code?**
**A:** No! Understanding the concepts is enough. Your value is translating business needs into clear, precise requirements that developers can implement.

**Q: How detailed should my requirements be?**
**A:** Detailed enough that a developer can build it without asking you questions. Include field names, data transformations, error handling, and what happens in edge cases.

---

## Resources for Continued Learning

### Reference Materials
- **HTTP Basics:** `docs/http_basics.md` - Complete HTTP reference guide
- **REST Principles:** `docs/rest_principles.md` - REST design patterns
- **Live API Documentation:** http://localhost:5001/api/docs - Interactive Swagger UI
- **Postman Collection:** `postman/TAFE_Student_API.postman_collection.json` - Ready-to-use requests

### Quick Reference

**HTTP Methods:**
- GET = Read/Retrieve data
- POST = Create new data
- PUT = Update existing data
- DELETE = Remove data

**Common Status Codes:**
- 200 = Success
- 201 = Created successfully
- 400 = Bad request (your data was wrong)
- 404 = Not found
- 409 = Conflict (duplicate data)
- 500 = Server error (their problem)

**Requirements Checklist:**
- [ ] Endpoint and method clearly specified
- [ ] All required fields identified
- [ ] Data transformations documented
- [ ] Error handling planned
- [ ] Edge cases considered
- [ ] Empty states defined

---

## Your Next Steps

1. **Practice more** - Use the student API to try different scenarios
2. **Apply what you learned** - Use the requirements template on your next project
3. **Share with your team** - Teach your colleagues what you discovered
4. **Always validate** - Test your assumptions with real API calls

---

### Final Thought

Understanding how APIs work makes you a more effective Business Analyst. You'll write clearer requirements, catch issues earlier, and communicate better with technical teams. The key is focusing on what the business needs and translating that into precise, implementable requirements.

**Happy requirement writing!** 🚀
