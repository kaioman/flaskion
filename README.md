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
