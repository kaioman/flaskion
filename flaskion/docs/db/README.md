# Database Documentation

This Directory contains the database specifications for the Uwgen application.
All documents here serve as **human-readable contracts** that describe the structure, purpose, and evolution of Uwgen's persistent data layer.

## Purpose

The goal of this documentation is to:

- Provide a clear and explicit description of each database table.
- Ensure future collaborators can understand the intent behind the schema.
- Maintain a stable contract between the application layer and the database layer.
- Support long-term maintainability and onboarding.

## Structure

```text
docs/db/ 
  ├── README.md        ← Overview of the database documentation 
  └── users.md         ← Specification for the `users` table
```

Additional tables should follow the same documentation format and be added to this directory as the system evolves.

## Related Artifacts

Database documentation is complemented by:

- **DDL files** in `db/schema/`
  (Static SQL definitions for schema creation)

- **Alembic migrations** in `/alembic/`
  (Versioned schema evolution)

These three layers together form Uwgen's complete database contract.

## Conventions

- All table documentation must be written in English.
- All timestamps use UTC unless otherwise specified.
- Primary keys should use UUID unless there is a strong reason not to.
- Sensitive data (e.g., passwords, API keys) must never be stored in plaintext.

## Versioning

Schema changes must be reflected in:

1. The relevant Markdown table specification
2. The DDL files
3. The Alembic migration scripts

This ensures consistency across documentation, development, and production environments.
