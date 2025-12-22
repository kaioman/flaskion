# Description

Flaskion is a lightweight and extensible API server designed to connect with multiple AI backends such as Gemini and OpenAI. It provides a unified interface for intelligent interactions.

## Remote Debugging Flask in Docker with VSCode

This project supports remote debugging of a Flask application running inside a Docker container using **VSCode** and **debugpy**.
The debugger is enabled only in the **development environment**.

## Setup

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
source .env/Scripts/activate # Windows
# or
source .env/bin/activate # Linux / macOS

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

```Jsonc
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

> 💡Tip: If you want to  debug both backend and frontend together, choose the compound configuration **Debug Flask + Chrome**. This will attach to the Flask process and simultaneously launch Chrome pointing to `http://localhost:5100`.

## Database Migration with Alembic

Flaskion use **Alembic** to manage database schema migrations in a consistent and reproducible way.
This section describes how to install, initialize, and run Alembic inside the Docker-based development environment.

### 1. Install Alembic (container)

Enter the Flaskion container and install Alembic into the virtual environment:

```bash
docker exec -it <container_name> bash
source .env/bin/activate
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

This creates a `alembic/` directory containing:

- `env.py` ー Alembic environment configuration
- `script.py.mako` ー migration script template
- `versions/` ー migration files will be stored here

### 3. Configure Alembic(`alembic.ini` and `env.py`)

Update `alembic.ini` to point to your database URL.
If Flaskion loads the DB URL from environment variables, set:

```Ini
sqlalchemy.url = ${DATABASE_URL}
```

Then modify `alembic/env.py` to load the SQLAlchemy `Base` from your application:

```Python
from flaskion.db import Base  # adjust import path as needed
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
