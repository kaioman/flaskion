# API Response Specification

This document defines the unified `success` and `error` response formats used across the Uwgen API.

## 1. Success Response

### Overview of Success Response

A success response is represented by the `SuccessResponse` model and returned in the following format.

### Response Format of Success Response

```json
{
    "data": { ... },
    "message": "optional success message",
    "meta": { ... }
}
```

### Response Fields

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| **data** | any | Yes | Main response payload |
| **message** | string | No | Optional human-readable success message |
| **meta** | object | No | Additional metadata (e.g., pagination info) |

### Example: User Signup Success

```json
{
    "data": {
        "id": 1,
        "email": "user@example.com"
    },
    "message": "User created successfully."
}
```

## 2. Error Response

### Overview

An error response is represented by the `ErrorResponse` model and returned in the following format.

### Response Format of Error Response

```json
{
    "errors": "error_code",
    "message": "error message",
    "details": { ... }
}
```

### Field Definitions

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| **errors** | string | Yes | Error code(Enum `.value`) |
| **message** | string | Yes | Human-readable error message |
| **details** | object | No | Additional information (e.g., validation errors) |

### Example: Validation Error

```json
{
    "errors": "invalid_request",
    "message": "The request payload is invalid.",
    "details": {
        "email": ["Not a valid email address."]
    }
}
```

### Example: Authentication Error

```json
{
    "errors": "invalid_credentials",
    "message": "Invalid email or password."
}
```

## 3. Error Code List

### AuthError

| Error Code | Message | Description |
| :--- | :--- | :--- |
| **email_exists** | This email is already registered. | Email already in use |
| **invalid_credentials** | Invalid email or password. | Authentication failed |
| **inactive_account** | Account is inactive. | Account disabled |

### RequestError

| Error Code | Message | Description |
| :--- | :--- | :--- |
| **invalid_request** | The request payload is invalid. | Invalid or malformed request |

## 4. HTTP Status Code Policy

| Status Code | Usage |
| :--- | :--- |
| **200 OK** | Standard success response |
| **201 Created** | Resource successfully created |
| **400 Bad Request** | Validation or request format error |
| **401 Unauthorized** | Authentication failure |
| **403 Forbidden** | Account inactive or insufficient permissons |
| **409 Conflict** | Resource conflict (e.g., email already exists) |

## 5. Common Specifications

### Content-Type

```text
application/json; charset=utf-8
```

### Timezone

```text
UTC
```

### Error Response Format

All errors MUST be returned in JSON format.
HTML error pages MUST NOT be returned.

The terms **MUST**, **MUST NOT**, and **SHOULD** follow the definitions in **RFC 2119**.

## 6. Future Extensions (Optional)

The response models are designed to support future enhancements such as:

- `trace_id` for request tracking
- `timestamp` for debugging
- `version` for API versioning
- `links` for HATEOAS-style navigation
- Standardized pagination metadata
