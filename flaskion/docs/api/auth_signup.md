# Signup API Specification

## Endpoint

POST /api/v1/auth/signup

## Request Body

```json
{
  "email": "user@example.com",
  "password": "PlainPassword123!"
}
```

## Success Response (201)

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2025-01-01T12:34:56Z",
  "updated_at": "2025-01-01T12:34:56Z"
}
```

## Error Responses

### 400 invalid_request

```json
{
  "error": "invalid_request",
  "message": "Email format is invalid."
}
```

### 409 email_exists

```json
{
  "error": "email_exists",
  "message": "This email is already registered."
}
```

### 422 weak_password

```json
{
  "error": "weak_password",
  "message": "Password must contain at least 8 characters."
}
```

## Validation Rules

- email: required, RFC5322, unique
- password: required, >= 8 chars

## Security Notes

- Password must be hashed using bcrypt or PBKDF2.
- No plaintext passwords.
