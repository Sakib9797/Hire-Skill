# HireSkill API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "candidate"
}
```

**Required Fields:**
- `email` (string): Valid email address
- `password` (string): Min 8 chars, 1 uppercase, 1 lowercase, 1 number

**Optional Fields:**
- `first_name` (string)
- `last_name` (string)
- `role` (string): `user`, `candidate`, `employer`, or `admin` (default: `user`)

**Success Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "candidate",
      "is_active": true,
      "created_at": "2026-01-27T10:30:00",
      "profile": {
        "id": 1,
        "bio": null,
        "phone": null,
        "location": null,
        "skills": [],
        "interests": [],
        "theme_preference": "light"
      }
    }
  }
}
```

**Error Responses:**
- `409`: Email already registered
- `422`: Validation error (invalid email, weak password, etc.)

---

### Login

Authenticate user and receive JWT tokens.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "candidate",
      "is_active": true,
      "profile": { ... }
    }
  }
}
```

**Error Responses:**
- `401`: Invalid email or password
- `403`: Account is deactivated

**Token Information:**
- Access Token: Expires in 1 hour (3600 seconds)
- Refresh Token: Expires in 30 days (2592000 seconds)

---

### Refresh Access Token

Get a new access token using a refresh token.

**Endpoint:** `POST /auth/refresh`

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Responses:**
- `401`: Invalid or expired refresh token
- `404`: User not found
- `403`: Account is deactivated

---

### Get Current User

Retrieve authenticated user information.

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "candidate",
      "is_active": true,
      "created_at": "2026-01-27T10:30:00",
      "profile": { ... }
    }
  }
}
```

---

## 👤 User Profile Endpoints

### Get User Profile

Get current user's profile.

**Endpoint:** `GET /users/profile`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "candidate",
      "is_active": true,
      "created_at": "2026-01-27T10:30:00",
      "profile": {
        "id": 1,
        "bio": "Full-stack developer with 5 years of experience",
        "phone": "+1234567890",
        "location": "New York, NY",
        "avatar_url": null,
        "skills": ["Python", "React", "PostgreSQL"],
        "experience": [],
        "education": [],
        "interests": ["AI", "Machine Learning"],
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "github_url": "https://github.com/johndoe",
        "portfolio_url": "https://johndoe.com",
        "theme_preference": "dark"
      }
    }
  }
}
```

---

### Update User Profile

Update current user's profile information.

**Endpoint:** `PUT /users/profile` or `PATCH /users/profile`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Full-stack developer passionate about building scalable applications",
  "phone": "+1234567890",
  "location": "San Francisco, CA",
  "skills": ["Python", "Flask", "React", "PostgreSQL", "Docker"],
  "interests": ["AI", "Web Development", "Open Source"],
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "github_url": "https://github.com/johndoe",
  "portfolio_url": "https://johndoe.com"
}
```

**All Fields are Optional:**
- `first_name` (string)
- `last_name` (string)
- `bio` (string)
- `phone` (string)
- `location` (string)
- `avatar_url` (string)
- `skills` (array of strings)
- `experience` (array of objects)
- `education` (array of objects)
- `interests` (array of strings)
- `linkedin_url` (string)
- `github_url` (string)
- `portfolio_url` (string)
- `theme_preference` (string): `light` or `dark`

**Success Response (200):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "user": { ... }
  }
}
```

---

### Update Theme Preference

Update user's theme preference.

**Endpoint:** `PUT /users/profile/theme`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "theme": "dark"
}
```

**Values:**
- `light`: Light theme
- `dark`: Dark theme

**Success Response (200):**
```json
{
  "success": true,
  "message": "Theme updated successfully",
  "data": {
    "theme_preference": "dark"
  }
}
```

---

## 👥 Admin Endpoints

### Get All Users

Retrieve paginated list of all users (admin only).

**Endpoint:** `GET /users/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 10)
- `role` (string, optional): Filter by role

**Example:**
```
GET /users/?page=1&per_page=20&role=candidate
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": {
    "users": [ ... ],
    "total": 50,
    "pages": 5,
    "current_page": 1,
    "per_page": 10
  }
}
```

**Error Response:**
- `403`: Insufficient permissions (not admin)

---

### Get User by ID

Retrieve specific user by ID (admin only).

**Endpoint:** `GET /users/<user_id>`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "user": { ... }
  }
}
```

**Error Responses:**
- `404`: User not found
- `403`: Insufficient permissions

---

## 🏥 Health Check

### Check API Status

Check if API is running.

**Endpoint:** `GET /health`

**No Authentication Required**

**Success Response (200):**
```json
{
  "status": "healthy",
  "message": "HireSkill API is running"
}
```

---

## 📋 Error Response Format

All error responses follow this structure:

```json
{
  "success": false,
  "message": "Error description",
  "errors": {
    "field_name": "Specific error message"
  }
}
```

### Common HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `409`: Conflict (e.g., email already exists)
- `422`: Unprocessable Entity (validation error)
- `500`: Internal Server Error

---

## 🔑 Role-Based Access

### Roles:
- `user`: Basic user access
- `candidate`: Job seeker profile
- `employer`: Company/recruiter profile
- `admin`: Full system access

### Access Control:
- Public endpoints: Register, Login, Health Check
- Authenticated endpoints: Profile management, Get current user
- Admin endpoints: Get all users, Get user by ID

---

## 📝 Examples

### cURL Examples

**Register:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "candidate"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Get Profile:**
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <access_token>"
```

**Update Profile:**
```bash
curl -X PUT http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Full-stack developer",
    "skills": ["Python", "React"],
    "interests": ["AI", "Web Dev"]
  }'
```

### JavaScript/Axios Examples

**Register:**
```javascript
const response = await axios.post('/api/auth/register', {
  email: 'user@example.com',
  password: 'SecurePass123',
  first_name: 'John',
  last_name: 'Doe',
  role: 'candidate'
});
```

**Login:**
```javascript
const response = await axios.post('/api/auth/login', {
  email: 'user@example.com',
  password: 'SecurePass123'
});
const { access_token, refresh_token, user } = response.data.data;
```

**Update Profile (with token):**
```javascript
const response = await axios.put('/api/users/profile', {
  bio: 'Full-stack developer',
  skills: ['Python', 'React', 'PostgreSQL'],
  interests: ['AI', 'Web Development']
}, {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});
```

---

## 🔒 Security Notes

1. **Always use HTTPS in production**
2. **Store tokens securely** (httpOnly cookies or secure storage)
3. **Never expose JWT secret keys**
4. **Implement rate limiting** for authentication endpoints
5. **Validate all input** on both client and server
6. **Use environment variables** for sensitive configuration
7. **Regularly rotate JWT secret keys**
8. **Implement token blacklisting** for logout functionality
9. **Monitor for suspicious activity**
10. **Keep dependencies updated**
