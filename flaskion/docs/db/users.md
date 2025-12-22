# `users` Table Specification

## Overview

The `users` table stores account information for Ugen users.
It represents the core identity record for authentication, authorization, and user-specific configuration.

This table is designed with the following goals:

- Security: no plaintext passwords or API keys.
- Extensibility: future fields can be added without breaking existing contracts.
- Clarity: each field has clear purpose and rationale.

---

## Table Definition

| Column Name        | Type        | Not Null | Unique | Default                | Description                          |
|--------------------|-------------|----------|--------|------------------------|--------------------------------------|
| id                 | UUID        | YES      | YES    | `gen_random_uuid()`    | Primary key for the user             |
| email              | TEXT        | YES      | YES    |                        | Login identifier for the user        |
| password_hash      | TEXT        | YES      | NO     |                        | Hashed password (bcrypt/argon2)      |
| is_active          | BOOLEAN     | YES      | NO     | `TRUE`                 | Whether the account is active        |
| created_at         | TIMESTAMPZ  | YES      | NO     | `NOW()`                | Account creation timestamp           |
| updated_at         | TIMESTAMPZ  | YES      | NO     | `NOW()`                | Last update timestamp                |
| last_login_at      | TIMESTAMPZ  | NO       | NO     |                        | Timestamp of the most recent login   |
| api_key_encrypted  | TEXT        | NO       | NO     |                        | Encrypted Gemini API key (optional)  |
| api_key_updated_at | TIMESTAMPZ  | NO       | NO     |                        | Timestamp of the last API key update |

## Indexes

- `users_pkey` - Primary key on `id`
- `users_email_key` - Unique index on `email`

---

## Security Notes

- `password_hash` must be generated using a secure hashing algorithm such as **bcrypt** or **argon2**.
- `api_key_encrypted` must be encrypted using AES-256 or equivalent.
- Decryption keys must be stored in environment variables, not in the database.
- API keys must never appear in logs, error messages, or plaintext storage.

---

## Lifecycle Events

- **Account creation** sets `created_at` and `updated_at`.
- **Profile updates** modify `updated_at`.
- **Successful login** updates `last_login_at`.
- **API key updates** modify both `api_key_encrypted` and `api_key_updated_at`.

---

## Future Extensions

Potential future fields include:

- `display_name`
- `avatar_url`
- `two_factor_secret`
- `role` (e.g., admin, standard user)
- `preferences` (JSONB)
  
These can be added without breaking existing contracts.

---

## Rationale

The `users` table is intentionally minimal yet secure.
It provides a stable foundation for authentication while allowing Uwgen to grow into more advanced account features over time.
