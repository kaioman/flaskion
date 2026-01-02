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

Uwgen's database schema is defined and initialized through the following artifacts:

### **DDL files**

  Static SQL definitions for database creation and schema initialization are located in:

```text
/docker-container/postgres-init/
  ├── 01-create-db.sql    ← Database creation
  └── 02-init-db.sql      ← Initial schema definitions
```

These files are executed automatically when the PostgreSQL container is first initialized.

### **Schema migrations**

Uwgen does not currently use Alembic for schema versioning.
If schema evolution becomes necessary in the future, Alembic (or another migration tool) may be introduced.
Any future migration system must remain consistent with the documentation in this directory.

## Conventions

- All table documentation must be written in English.
- All timestamps use UTC unless otherwise specified.
- Primary keys should use UUID unless there is a strong reason not to.
- Sensitive data (e.g., passwords, API keys) must never be stored in plaintext.
- Authentication token (JWT) are **not** stored in the database.
  Uwgen uses stateless JWT-based authentication, and the database stores only persistent user information.

## Versioning

Schema changes must be reflected in:

1. The relevant Markdown table specification
2. The DDL files in `/docker-container/postgres-init/`
3. Any future migration scripts (if a migration system is introduced)

This ensures consistency across documentation, development, and production environments.

---
