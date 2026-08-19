# API Documentation
## BloodLife REST API

Base URL: `http://localhost:5000`

---

## GET /api/stats
Get website statistics.

**Response:**
```json
{
    "total": 12,
    "available": 10,
    "locations": ["Dhanmondi, Dhaka", "Gulshan, Dhaka"],
    "blood_counts": {"A+": 3, "B+": 2, "O+": 4, "AB+": 1, "A-": 1, "B-": 1}
}
```

---

## GET /api/donors
List all donors. Supports filters.

**Query Parameters:**
- `search` - Search by name, location, or phone
- `blood` - Filter by blood group (A+, B+, etc.)
- `location` - Filter by location

**Example:** `GET /api/donors?blood=A+&search=dhaka`

**Response:**
```json
[
    {
        "id": 1,
        "name": "Ahmed Rahman",
        "blood_group": "A+",
        "phone": "01712345678",
        "email": "ahmed@email.com",
        "location": "Dhanmondi, Dhaka",
        "address": "House 12, Road 5",
        "age": 28,
        "gender": "Male",
        "is_available": 1,
        "created_at": "2026-01-15 10:30:00"
    }
]
```

---

## POST /api/donors
Add a new donor.

**Request Body (JSON):**
```json
{
    "name": "New Donor",
    "blood_group": "B+",
    "phone": "01812345679",
    "email": "donor@email.com",
    "location": "Gulshan, Dhaka",
    "address": "House 5",
    "age": 25,
    "gender": "Male"
}
```

**Required fields:** name, blood_group, phone, location

**Response (201):**
```json
{"message": "Donor registered successfully!", "id": 13}
```

**Error (400):**
```json
{"error": "Name, blood group, phone, and location are required"}
```

---

## DELETE /api/donors/:id
Delete a donor. Requires admin login.

**Example:** `DELETE /api/donors/1`

**Response:**
```json
{"message": "Donor deleted"}
```

**Error (401):**
```json
{"error": "Not logged in"}
```

---

## POST /api/login
Admin login.

**Request Body:**
```json
{
    "username": "admin",
    "password": "admin123"
}
```

**Response:**
```json
{"message": "Login successful"}
```

**Error (401):**
```json
{"error": "Invalid username or password"}
```

---

## POST /api/logout
Admin logout.

**Response:**
```json
{"message": "Logged out"}
```
