# Signin API Specification

## Endpoint

POST /api/v1/auth/signin

## Request Body

```json
{
  "email": "user@example.com",
  "password": "PlainPassword123!"
}
```

## Success Response (200)

```json
{
  "access_token": "jwt_token_here",
  "token_type": "Bearer"
}
```

## Error Responses

### 401 unauthorized

```json
{
  "error": "invalid_credentials",
  "message": "Email or password is incorrect."
}
```

### 403 forbidden

```json
{
  "error": "inactive_account",
  "message": "This account exists but is not active."
}
```

### 400 bad_request

```json
{
  "error": "invalid_request",
  "message": "Email format is invalid."
}
```

## Validation Rules

- email: required, RFC5322
- password: required

## Security Notes

- Password comparison must use a secure hashing algorithm (bcrypt/PBKDF2).
- No plaintext passwords.
- JWT must be signed using a secure secret key.
- Tokens must not include sensitive data.
