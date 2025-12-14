from app.main import app # noqa: F401

# NOTE:
# Do not remove 'app'. Although it looks unused in this file,
# Flask (`flask run`) and Gunicorn (`server:app`) rely on it as the entrypoint.
# It is required for the application to start correctly.

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
