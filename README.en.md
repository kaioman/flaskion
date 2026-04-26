# Flaskion - Unified AI Backend API Server

**Flaskion** is a lightweight and extensible Flask-based API server designed to provide a unified interface for connecting with multiple AI backends including **Gemini**, **ComfyUI**, and other intelligent services.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Remote Debugging Flask in Docker with VSCode](#remote-debugging-flask-in-docker-with-vscode)
- [Database Migration with Alembic](#database-migration-with-alembic)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

Flaskion acts as a centralized API gateway that abstracts the complexity of managing multiple AI service integrations. It provides:

- **Unified REST API** for text generation, image generation, and image analysis
- **Multi-backend support** (Gemini, ComfyUI, etc.)
- **Database persistence** with PostgreSQL and SQLAlchemy
- **Authentication & Security** with JWT and encrypted credentials
- **Extensible architecture** for adding new services and features
- **Docker-first deployment** with development and production profiles

## Features

- ✅ Multi-AI backend integration (Gemini, ComfyUI)
- ✅ Unified REST API for text and image operations
- ✅ PostgreSQL database with Alembic migrations
- ✅ Remote debugging support via VSCode + debugpy
- ✅ Docker Compose for local development
- ✅ Credential management with Fernet encryption
- ✅ Comprehensive logging and error handling
- ✅ Request/Response validation with Marshmallow schemas
- ✅ RESTful service architecture

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python** 3.11 or higher
- **Docker** 20.10+ and **Docker Compose** 1.29+
- **PostgreSQL** 12+ (or use Docker version)
- **Git** for version control

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kaioman/flaskion.git
cd flaskion
```

### 2. Set Up Virtual Environment

#### On Windows

```bash
python -m venv env
env\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
pip install debugpy  # For development/debugging
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/flaskion_db

# AI Backends
GEMINI_API_KEY=your_gemini_api_key
COMFYUI_URL=http://localhost:8188

# Flask
FLASK_APP=server.py
FLASK_ENV=development  # or production
SECRET_KEY=your_secret_key
FERNET_KEY=your_fernet_key  # Use gen_fernet_key.py

# Debugging (development only)
DEBUGPY=false
DEBUG_PORT=5150
```

### 5. Generate Encryption Keys (if needed)

For credential encryption:

```bash
python gen_fernet_key.py
python gen_secret_key.py
```

## Quick Start

### Option A: Docker Compose (Recommended)

```bash
# Build and start containers
docker-compose up -d

# Initialize database (first time)
docker exec -it flaskion bash
source env/bin/activate
alembic upgrade head
exit

# Flask API is now available at http://localhost:5100
```

### Option B: Local Development

```bash
# Ensure PostgreSQL is running locally
# Update DATABASE_URL in .env to point to your local instance

# Activate virtual environment
env\Scripts\activate  # Windows
# or
source env/bin/activate  # macOS/Linux

# Run migrations
alembic upgrade head

# Start Flask development server
python server.py
# or
flask run --host=0.0.0.0 --port=5100

# API is available at http://localhost:5100
```

## Project Structure

```bash
flaskion/
├── app/
│   ├── __init__.py              ← Flask application factory
│   ├── main.py                  ← Main application setup
│   ├── api/
│   │   └── v1/                  ← API v1 endpoints
│   │       ├── auth.py          ← Authentication endpoints
│   │       ├── text_gen.py      ← Text generation endpoints
│   │       ├── image_gen.py     ← Image generation endpoints
│   │       ├── image_edit.py    ← Image editing endpoints
│   │       └── image_analyze.py ← Image analysis endpoints
│   ├── services/
│   │   ├── auth_service.py      ← Auth business logic
│   │   ├── text_gen_service.py  ← Text generation logic
│   │   ├── image_gen_service.py ← Image generation logic
│   │   ├── image_edit_service.py← Image editing logic
│   │   └── image_analyze_service.py ← Image analysis logic
│   ├── models/
│   │   ├── user.py              ← SQLAlchemy User model
│   │   ├── request_log.py       ← Request logging model
│   │   └── ...                  ← Other database models
│   ├── schemas/
│   │   ├── auth.py              ← Auth request/response schemas
│   │   ├── text_gen.py          ← Text generation schemas
│   │   ├── image.py             ← Image operation schemas
│   │   └── ...                  ← Other validation schemas
│   ├── core/
│   │   ├── security.py          ← Password hashing, JWT tokens
│   │   ├── config.py            ← Configuration management
│   │   ├── constants.py         ← Application constants
│   │   └── exceptions.py        ← Custom exceptions
│   ├── db/
│   │   ├── session.py           ← SQLAlchemy session management
│   │   └── base.py              ← Base model configuration
│   ├── routes/
│   │   ├── auth.py              ← Auth route blueprints
│   │   ├── text_gen.py          ← Text generation routes
│   │   ├── image.py             ← Image operation routes
│   │   └── ...                  ← Other route blueprints
│   ├── static/                  ← Static files (CSS, JS, images)
│   ├── templates/               ← HTML templates (if using templates)
│   ├── test_api_*.py            ← Test files for API endpoints
│   └── configs/
│       ├── logger.json          ← Logging configuration
│       └── comfyui/             ← ComfyUI configuration
├── alembic/
│   ├── env.py                   ← Alembic environment configuration
│   ├── script.py.mako           ← Migration script template
│   ├── versions/                ← Database migration scripts
│   └── README                   ← Alembic documentation
├── docker-container/
│   ├── Dockerfile               ← Container image definition
│   ├── docker-compose.yml       ← Production compose config
│   ├── docker-compose.override.yml ← Development compose config
│   ├── exec-py311_flask.sh      ← Flask execution script
│   └── exec-pg12_uwgen.sh       ← PostgreSQL execution script
├── credentials/
│   └── gen-lang-client-*.json   ← Google Cloud credentials
├── server.py                    ← Application entry point
├── requirements.txt             ← Python dependencies
├── alembic.ini                  ← Alembic configuration
├── gen_fernet_key.py            ← Fernet key generator utility
├── gen_secret_key.py            ← Secret key generator utility
└── README.md                    ← This file (Japanese)
```

## API Endpoints

### Text Generation

- `POST /api/v1/text/generate` - Generate text using AI backend
- `GET /api/v1/text/models` - List available text generation models

### Image Generation

- `POST /api/v1/image/generate` - Generate image from text
- `POST /api/v1/image/generate-comfyui` - Generate using ComfyUI
- `GET /api/v1/image/models` - List available image generation models

### Image Editing

- `POST /api/v1/image/edit` - Edit an existing image
- `POST /api/v1/image/upscale` - Upscale image resolution

### Image Analysis

- `POST /api/v1/image/analyze` - Analyze image content
- `POST /api/v1/image/describe` - Generate description for image

### Authentication

- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/signin` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/refresh` - Refresh JWT token

## Remote Debugging Flask in Docker with VSCode

This project supports remote debugging of a Flask application running inside a Docker container using **VSCode** and **debugpy**.
The debugger is enabled only in the **development environment**.

### 1. Install `debugpy` in the container

Enter the remote container and activate the virtual environment:

```bash
docker exec -it <container_name> bash
source .env/bin/activate
pip install debugpy
```

This ensures that the Flask process inside the container can start with debugpy.

### 2. Install `debugpy` on the host (development only)

Since the source code imports `debugpy`, the host environment also needs the
package to avoid import errors when editing or running tools locally.

Activate your host virtual environment and install:

```bash
env\Scripts\activate  # Windows
# or
source env/bin/activate  # macOS/Linux

pip install debugpy
```

### 3. Expose the debugger port

In `docker-compose.override.yml` (development only):

```yaml
services:
  flaskion:
    ports:
      - "5100:5100" # Flask
      - "5150:5150" # for debugging
    environment:
      - DEBUGPY=true
      - DEBUG_PORT=5150 # debugger port
      - PYDEVD_DISABLE_FILE_VALIDATION=1
    entrypoint: [
      "/var/docker-flask/flaskion/env/bin/python", 
      "-Xfrozen_modules=off", 
      "-m", "flask",
    ]
    command: [
      "run",
      "--host=0.0.0.0",
      "--port=5100"
    ]
```

### 4. Enable `debugpy` in `server.py`

Add the following snippet at the top of your entrypoint(`server.py`):

```python
# debugpy
import os

# Debug mode check
if os.getenv("DEBUGPY", "false").lower() == "true":
    # Prevent duplicate listen
    if not os.getenv("DEBUGPY_STARTED"):
        os.environ["DEBUGPY_STARTED"] = "true"
        import debugpy
        
        # Get debug port
        debug_port = int(os.getenv("DEBUG_PORT", "5150"))
        print(f"🚀[debugpy] Preparing to open listener on port {debug_port}")
        # Listen on debug port
        debugpy.listen(("0.0.0.0", debug_port))
        print(f"✅[debugpy] Client connected. Continuing execution.")
```

### 5. Configure `launch.json` in VSCode

Finally, configure VSCode to attach to the Flask process running inside Docker.
Add the following to `.vscode/launch.json`

```jsonc
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "debugpy",
            "request": "attach",
            "name": "Attach to Flask (Docker)",
            "connect": {
                "host": "localhost",
                "port": 5150
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/flaskion",
                    "remoteRoot": "/var/docker-flask/flaskion"
                }
            ]
        },
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome for localhost",
            "url": "http://localhost:5100",
            "webRoot": "${workspaceFolder}"
        }
    ],
    "compounds": [
        {
            "name": "Debug Flask + Chrome",
            "configurations": [
                "Attach to Flask (Docker)",
                "Launch Chrome for localhost"
            ]
        }
    ]
}
```

This configuration allows you to attach VSCode's debugger to the Flask app
inside Docker and simultaneously launch Chrome for frontend debugging.

### 6. Attach VSCode to the Flask process

Once the container is running with `debugpy` enabled and the port exposed:

1. Open VSCode and go to the **Run and Debug** panel (`Ctrl+Shift+D`).
2. From the dropdown, select **Attach to Flask (Docker)** (or the compound **Debug Flask + Chrome** if you want to debug both backend and frontend).
3. Press **Start Debugging** (F5).
4. VSCode will connect to the Flask process inside the Docker container via port `5150`
5. Set breakpoints in your Python source files. When the Flask app executes those lines, VSCode will pause execution and allow you to inspect variables, stack traces, and more.
6. To stop debugging, simply stop the session in VSCode. The Flask app continues running inside the container.

> 💡 **Tip**: If you want to debug both backend and frontend together, choose the compound configuration **Debug Flask + Chrome**. This will attach to the Flask process and simultaneously launch Chrome pointing to `http://localhost:5100`.

## Database Migration with Alembic

Flaskion uses **Alembic** to manage database schema migrations in a consistent and reproducible way.
This section describes how to install, initialize, and run Alembic inside the Docker-based development environment.

### 1. Install Alembic (container)

Enter the Flaskion container and install Alembic into the virtual environment:

```bash
docker exec -it <container_name> bash
source env/bin/activate
pip install alembic
```

If you are using a requirements file, also update it:

```bash
pip freeze > requirements.txt
```

### 2. Initialize Alembic

Inside the container, initialize Alembic:

```bash
alembic init alembic
```

This creates an `alembic/` directory containing:

- `env.py` — Alembic environment configuration
- `script.py.mako` — migration script template
- `versions/` — migration files will be stored here

### 3. Configure Alembic (`alembic.ini` and `env.py`)

Update `alembic.ini` to point to your database URL.
If Flaskion loads the DB URL from environment variables, set:

```ini
sqlalchemy.url = ${DATABASE_URL}
```

Then modify `alembic/env.py` to load the SQLAlchemy `Base` from your application:

```python
from app.db import Base  # adjust import path as needed
target_metadata = Base.metadata
```

This ensures Alembic can autogenerate migrations based on your models.

### 4. Create a Migration

To generate a migration based on model changes:

```bash
alembic revision --autogenerate -m "describe your change"
```

Alembic will create a new file under `alembic/versions/`.
Review the generated migration script to ensure correctness.

### 5. Apply Migrations

Run migrations inside the container:

```bash
alembic upgrade head
```

To downgrade:

```bash
alembic downgrade -1
```

### 6. Running Alembic in Docker Compose

If you want Alembic to run automatically on container startup (optional),
add a command to your `docker-compose.override.yml`:

```yaml
command: >
  bash -c "
    alembic upgrade head &&
    flask run --host=0.0.0.0 --port=5100
  "
```

This ensures the database schema is always up-to-date in development.

## Testing

Run the included test files to validate API endpoints:

```bash
# Text generation API test
python -m pytest app/test_api_text_gen.py -v

# Image generation API test
python -m pytest app/test_api_image_gen.py -v

# Image generation with ComfyUI API test
python -m pytest app/test_api_image_gen_comfyui.py -v

# Image editing API test
python -m pytest app/test_api_image_edit.py -v

# Image analysis API test
python -m pytest app/test_api_image_analyze.py -v
```

## Troubleshooting

### Issue: Flask app won't start in Docker

**Solution:**

- Ensure `docker-compose.override.yml` has the correct paths
- Check that environment variables are properly set
- Verify PostgreSQL container is running: `docker ps`

### Issue: Database connection errors

**Solution:**

- Confirm DATABASE_URL is correct in `.env`
- Check PostgreSQL container logs: `docker logs postgres`
- Ensure database exists and migrations have been run

### Issue: debugpy connection fails

**Solution:**

- Verify port 5150 is exposed in docker-compose
- Check that DEBUGPY=true is set in environment
- Ensure VSCode launch.json pathMappings are correct

### Issue: Import errors for missing modules

**Solution:**

```bash
pip install -r requirements.txt
```

### Issue: Fernet or Secret key errors

**Solution:**

```bash
python gen_fernet_key.py
python gen_secret_key.py
# Update .env with generated keys
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainers.

---

**Last Updated**: 2026-04-26
