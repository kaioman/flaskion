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

| Column Name               | Type        | Not Null | Unique | Default                | Description                                 |
|---------------------------|-------------|----------|--------|------------------------|---------------------------------------------|
| id                        | UUID        | YES      | YES    | `gen_random_uuid()`    | Primary key for the user                    |
| email                     | TEXT        | YES      | YES    |                        | Login identifier for the user               |
| password_hash             | TEXT        | YES      | NO     |                        | Hashed password (bcrypt/argon2)             |
| is_active                 | BOOLEAN     | YES      | NO     | `TRUE`                 | Whether the account is active               |
| created_at                | TIMESTAMPZ  | YES      | NO     | `NOW()`                | Account creation timestamp                  |
| updated_at                | TIMESTAMPZ  | YES      | NO     | `NOW()`                | Last update timestamp                       |
| last_login_at             | TIMESTAMPZ  | NO       | NO     |                        | Timestamp of the most recent login          |
| uwgen_api_key             | TEXT        | NO       | NO     |                        | Uwgen API key (plaintext)                   |
| uwgen_api_key_updated_at  | TIMESTAMPZ  | NO       | NO     |                        | Timestamp of the last Uwgen API key update  |
| gemini_api_key_encrypted  | TEXT        | NO       | NO     |                        | Encrypted Gemini API key (optional)         |
| gemini_api_key_updated_at | TIMESTAMPZ  | NO       | NO     |                        | Timestamp of the last Gemini API key update |

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

## Updatable Field Metadata

To ensure both safety and extensiblity in user-settings updates, Uwgen uses SQLAlchemy's
`Column.info` metadata to explicitly mark which fields are allowed to be updated through the
settings API.

### Purpose

The `PATCH /api/v1/settings` endpoint accepts partial updates from the client.
Allowing arbitrary JSON keys to directly modify model attributes introduces two major risks:

1. **Security risk** ー Sensitive fields such as `email`, `password_hash`, `role`, or `id` could be overwritten if not explicitly protected.
2. **Maintenance risk** ー Hard-coding a list of updatable fields in service logic can lead to silent failures when new fields are added but not registered.

To avoid both problems, the model itself declares which fields are safe to update.

### How It Works

Each updatable column includes a metadata flag:

```Python
api_key_encrypted = Column(
    Text,
    info={"updatable": True}
)
```

The service layer then derives the list of updatable fields directly from the model:

```Python
updatable_fields = {
    col.key
    for col in User.__table__.columns
    if col.info.get("updatable")
}
```

During a settings update, only fields in this whitelist are applied.

```Python
for key, value in updates.items():
    if key in updatable_fields and value is not None:
        setattr(user, key, value)
```

### Benefits of Updatable

- **Security**
  Prevents accidental or malicious modification of protected fields such as `id`, `email`, or `password_hash`.
- **Extensibility**
  Adding a new user-configurable field requires only updating the model definition.
  No changes are needed in the service or routing layers.
- **Single Source of Truth**
  The model defines which fields are safe to update, keeping the contract clear and centralized.
- **No Database Migration Required**
  `Column.info` is ORM-level metadata and does not affect the database schema.
  Adding or modifying `info` values does not require Alembic migrations.

---

## Encryption Metadata (`encrypt` and `key`)

Some user fields contain sensitive API keys that must be encrypted before being stored in the database.
To support this securely and declaratively, the `users` model uses two additional `Column.info` metadata flags:

### `encrypt: True`

When present, this flag indicates that the field must be encrypted before being persisted.
The service layer checks this metadata during settings updates:

- If `encrypt=True`, the incoming plaintext value is encrypted using the appropriate Fernet cipher.
- If `encrypt` is not set, the value is stored as-is.

This ensures that encryption behavior is defined at the model level rather than scattered across service logic.

### `key: EncryptionKeyType`

Encrypted fields must specify which Fernet encryption key should be used.
Uwgen supports multiple Fernet keys (e.g., one for Uwgen API keys, one for Gemini API keys).
The `key` metadata associates a field with the correct key:

```Python
info={"updatable": True, "encrypt": True, "key": EncryptionKeyType.UWGEN}
```

During updates, the service layer reads this metadata and selects the appropriate cipher instance.

### Benefits of Encryption

- **Security**
  Ensures that sensitive fields are always encrypted with the correct key, with no risk of
  accidental plaintext storage.
- **Explicit Contracts**
  The model clearly declares which fields require encryption and which key they use.
- **Extensibility**
  Adding a new encrypted field requires only updating the model definition;
  no changes are needed in the service layer.
- **Environment Isolation**
  Each key type maps to a different Fernet key, allowing development and production
  environments to use separate encryption keys safely.
  
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
