# 🧪 Testing Guide for HireSkill

## Manual Testing Checklist

### ✅ User Registration Flow

1. **Navigate to Registration**
   - [ ] Open http://localhost:3000
   - [ ] Click "Get Started" or navigate to /register
   - [ ] Registration form displays correctly

2. **Test Valid Registration**
   - [ ] Enter valid email: test@example.com
   - [ ] Enter strong password: TestPass123
   - [ ] Enter first name: Test
   - [ ] Enter last name: User
   - [ ] Select role: Candidate
   - [ ] Click "Create Account"
   - [ ] Success message displays
   - [ ] Redirects to login page after 2 seconds

3. **Test Password Validation**
   - [ ] Try password < 8 characters → Shows error
   - [ ] Try password without uppercase → Shows error
   - [ ] Try password without lowercase → Shows error
   - [ ] Try password without number → Shows error
   - [ ] Password strength indicator shows weak/medium/strong

4. **Test Email Validation**
   - [ ] Try invalid email format → Shows error
   - [ ] Try already registered email → Shows "Email already registered"

5. **Test Password Confirmation**
   - [ ] Enter mismatched passwords → Shows "Passwords do not match"
   - [ ] Enter matching passwords → No error

### ✅ User Login Flow

1. **Navigate to Login**
   - [ ] Navigate to /login
   - [ ] Login form displays correctly

2. **Test Valid Login**
   - [ ] Enter registered email
   - [ ] Enter correct password
   - [ ] Click "Sign In"
   - [ ] Redirects to dashboard
   - [ ] User data loads correctly

3. **Test Invalid Login**
   - [ ] Try wrong email → Shows error
   - [ ] Try wrong password → Shows error
   - [ ] Error message is user-friendly

4. **Test Form Validation**
   - [ ] Try empty email → Required field error
   - [ ] Try empty password → Required field error

### ✅ Dashboard & Profile Management

1. **View Dashboard**
   - [ ] Dashboard loads with user data
   - [ ] User name displays in navbar
   - [ ] User avatar/initials display correctly
   - [ ] Account info card shows correct data
   - [ ] Profile details card displays

2. **Edit Profile**
   - [ ] Click "Edit Profile" button
   - [ ] Form fields populate with existing data
   - [ ] Can edit first name
   - [ ] Can edit last name
   - [ ] Can edit bio
   - [ ] Can edit phone
   - [ ] Can edit location

3. **Manage Skills**
   - [ ] Add new skill → Displays in list
   - [ ] Add duplicate skill → Prevented
   - [ ] Remove skill → Removed from list
   - [ ] Add skill with Enter key works

4. **Manage Interests**
   - [ ] Add new interest → Displays in list
   - [ ] Add duplicate interest → Prevented
   - [ ] Remove interest → Removed from list
   - [ ] Add interest with Enter key works

5. **Save Profile**
   - [ ] Click "Save Changes"
   - [ ] Success message displays
   - [ ] Profile updates immediately
   - [ ] Updated data persists after refresh

6. **Cancel Edit**
   - [ ] Click "Cancel"
   - [ ] Returns to view mode
   - [ ] Changes are discarded

### ✅ Theme Toggle

1. **Test Theme Switching**
   - [ ] Click moon icon (🌙) → Switches to dark mode
   - [ ] Click sun icon (☀️) → Switches to light mode
   - [ ] Theme persists after page refresh
   - [ ] All components update colors correctly
   - [ ] Transitions are smooth

2. **Test Dark Mode**
   - [ ] Background is dark
   - [ ] Text is light
   - [ ] Buttons have correct colors
   - [ ] Cards have dark backgrounds
   - [ ] Borders are visible
   - [ ] All text is readable

3. **Test Light Mode**
   - [ ] Background is light
   - [ ] Text is dark
   - [ ] Buttons have correct colors
   - [ ] Cards have light backgrounds
   - [ ] Borders are visible
   - [ ] All text is readable

### ✅ Authentication & Security

1. **Test Protected Routes**
   - [ ] Try accessing /dashboard while logged out
   - [ ] Should redirect to /login
   - [ ] After login, redirects to dashboard

2. **Test Token Expiration**
   - [ ] Wait for token to expire (or manually delete)
   - [ ] Make authenticated request
   - [ ] Token auto-refreshes
   - [ ] Request completes successfully

3. **Test Logout**
   - [ ] Click "Logout" button
   - [ ] Redirects to login page
   - [ ] Tokens are cleared from localStorage
   - [ ] Cannot access protected routes

4. **Test Session Persistence**
   - [ ] Login successfully
   - [ ] Close and reopen browser
   - [ ] Still logged in (if within token lifetime)
   - [ ] Dashboard loads without re-login

### ✅ Role-Based Access (If Testing Admin Features)

1. **Create Admin User**
   - [ ] Use manage_db.py to create admin user
   - [ ] Login as admin
   - [ ] Can access /api/users/ endpoint
   - [ ] Can view all users

2. **Test Regular User Access**
   - [ ] Login as regular user
   - [ ] Try accessing /api/users/ → Gets 403 error
   - [ ] Cannot view other users

### ✅ Responsive Design

1. **Test on Desktop (1920x1080)**
   - [ ] Layout looks correct
   - [ ] All elements visible
   - [ ] Spacing is appropriate

2. **Test on Tablet (768x1024)**
   - [ ] Layout adjusts correctly
   - [ ] Navigation works
   - [ ] Forms are usable

3. **Test on Mobile (375x667)**
   - [ ] Single column layout
   - [ ] Buttons are large enough
   - [ ] Text is readable
   - [ ] Forms are usable
   - [ ] Cards stack vertically

### ✅ Error Handling

1. **Test Network Errors**
   - [ ] Stop backend server
   - [ ] Try to login → Shows appropriate error
   - [ ] Try to update profile → Shows error
   - [ ] Error messages are user-friendly

2. **Test Validation Errors**
   - [ ] Submit forms with invalid data
   - [ ] Errors display clearly
   - [ ] Error messages are helpful
   - [ ] Form can be corrected and resubmitted

### ✅ Browser Compatibility

Test in multiple browsers:
- [ ] Google Chrome
- [ ] Mozilla Firefox
- [ ] Microsoft Edge
- [ ] Safari (if on Mac)

For each browser, verify:
- [ ] Registration works
- [ ] Login works
- [ ] Theme toggle works
- [ ] Profile update works
- [ ] No console errors

---

## API Testing with cURL

### Test Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "first_name": "Test",
    "last_name": "User",
    "role": "candidate"
  }'
```

**Expected Response:**
- Status: 201 Created
- Contains user object and profile

### Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

**Expected Response:**
- Status: 200 OK
- Contains access_token and refresh_token

### Test Get Profile (Replace TOKEN with actual token)
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer TOKEN"
```

**Expected Response:**
- Status: 200 OK
- Contains user profile data

### Test Update Profile
```bash
curl -X PUT http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "bio": "New bio",
    "skills": ["Python", "React"],
    "interests": ["AI"]
  }'
```

**Expected Response:**
- Status: 200 OK
- Contains updated user data

### Test Theme Update
```bash
curl -X PUT http://localhost:5000/api/users/profile/theme \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"theme": "dark"}'
```

**Expected Response:**
- Status: 200 OK
- Confirms theme update

### Test Invalid Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "WrongPassword"
  }'
```

**Expected Response:**
- Status: 401 Unauthorized
- Error message

### Test Duplicate Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

**Expected Response:**
- Status: 409 Conflict
- "Email already registered" message

---

## Automated Testing

### Backend Unit Tests (Example)

```python
# tests/test_auth.py
import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register_user(client):
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    })
    assert response.status_code == 201
    assert response.json['success'] == True

def test_login_user(client):
    # First register
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    
    # Then login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json['data']
```

### Frontend Tests (Example)

```javascript
// src/__tests__/Login.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from '../pages/Login';

test('renders login form', () => {
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );
  
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
});

test('shows error on invalid login', async () => {
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );
  
  fireEvent.click(screen.getByRole('button', { name: /sign in/i }));
  
  // Assert error message appears
});
```

---

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test registration endpoint
ab -n 100 -c 10 -p register.json -T application/json \
  http://localhost:5000/api/auth/register

# Test login endpoint
ab -n 1000 -c 50 -p login.json -T application/json \
  http://localhost:5000/api/auth/login
```

### Expected Performance
- Registration: < 500ms per request
- Login: < 300ms per request
- Profile update: < 400ms per request
- Get profile: < 200ms per request

---

## Security Testing

### Test Password Security
- [ ] Passwords are hashed (never stored in plain text)
- [ ] Strong password requirements enforced
- [ ] Bcrypt salt rounds configured properly

### Test JWT Security
- [ ] Tokens have expiration times
- [ ] Tokens contain correct claims
- [ ] Refresh tokens work properly
- [ ] Invalid tokens are rejected

### Test Input Validation
- [ ] SQL injection attempts fail
- [ ] XSS attempts are sanitized
- [ ] Invalid JSON is rejected
- [ ] Missing required fields return 422

### Test CORS
- [ ] API accepts requests from localhost:3000
- [ ] API rejects requests from unauthorized origins

---

## Database Testing

### Test User Creation
```sql
-- Check if user was created
SELECT * FROM users WHERE email = 'test@example.com';

-- Check if profile was created
SELECT * FROM user_profiles WHERE user_id = (
  SELECT id FROM users WHERE email = 'test@example.com'
);
```

### Test Data Integrity
```sql
-- Check foreign key constraints
SELECT * FROM user_profiles WHERE user_id NOT IN (SELECT id FROM users);
-- Should return 0 rows

-- Check unique constraints
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
-- Should return 0 rows
```

---

## Common Issues & Solutions

### Issue: "Connection refused" error
**Solution:** Make sure PostgreSQL is running and database exists

### Issue: Token expired immediately
**Solution:** Check JWT_ACCESS_TOKEN_EXPIRES in .env

### Issue: CORS error in browser
**Solution:** Ensure backend CORS is configured for localhost:3000

### Issue: Password validation not working
**Solution:** Check password regex in validators.py

### Issue: Theme not persisting
**Solution:** Check localStorage access and API call

---

## Test Data

### Valid Test Users

```json
{
  "admin": {
    "email": "admin@hireskill.com",
    "password": "Admin123"
  },
  "candidate": {
    "email": "candidate@hireskill.com",
    "password": "Candidate123"
  },
  "employer": {
    "email": "employer@hireskill.com",
    "password": "Employer123"
  }
}
```

### Invalid Test Data

```json
{
  "weak_password": "pass",
  "no_uppercase": "password123",
  "no_number": "Password",
  "invalid_email": "notanemail",
  "empty_fields": {}
}
```

---

## Testing Completion Checklist

- [ ] All manual tests passed
- [ ] API tests return expected responses
- [ ] Error handling works correctly
- [ ] Theme toggle works in all pages
- [ ] Profile updates persist
- [ ] Authentication flow is secure
- [ ] Responsive design works on all sizes
- [ ] No console errors in browser
- [ ] No Python exceptions in backend
- [ ] Database constraints enforced

---

**Testing is complete when all items are checked and no critical issues remain.**
