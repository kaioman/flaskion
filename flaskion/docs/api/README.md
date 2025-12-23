# API Documentation

This Directory contains the API specifications for the Uwgen application.
All documents here serve as **human-readable contracts** that define how the
frontend and backend communicate.

## Purpose

The goals of this documentation are to:

- Provide clear and explicit API contracts.
- Ensure future collaborators can understand the intent behind each endpoint.
- Maintain consistency across UI, backend, and test.
- Support long-term maintainability and onboarding.

## Structure

```text
docs/api/
  ├── README.md ← Overview of the API documentation
  ├── auth_signup.md ← Signup API specification
  ├── auth_signin.md ← Signin API specification
```

## Design Principles

- **Contract-first**: API behavior is defined before implementation.
- **Predictable**: Similar endpoints behave in similar ways.
- **Consistent**: Naming, structure, and error formats are unified.
- **Secure by default**: No plaintext passwords, no sensitive data leakage.
- **Minimal but extensible**: Start small, grow safely.

## Conventions

### Endpoint Naming

- Base path: `/api/v1/`
- Resource-oriented, not verb-oriented.

### HTTP Methods

- `POST` for creation
- `GET` for retrieval
- `PATCH` for partial updates
- `DELETE` for deletion

### JSON Format

- All fields use `snake_case`
- All timestamps use UTC.
- Error responses follow this structure:

```json
{
  "error": "error_code",
  "message": "Human readable message"
}
```

## Authentication

- Authentication is handled via JWT(details TBD).
- Tokens are passed via the `Authorization: Bearer<token>` header.

## Versioning

Uwgen uses URL-based versioning:

- `/api/v1` is the current stable version.
- Breaking changes will introduce `/api/v2`.

## API List

- Authentication
  - Signup
  - Signin
