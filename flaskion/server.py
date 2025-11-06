import eventlet
import eventlet.wsgi
from app.main import app, observer

if __name__ == "__main__":
    try:
        eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 5150)), app)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
