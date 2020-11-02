from werkzeug.serving import run_simple

from app import app_factory

app = app_factory.create_app()

if __name__ == "__main__":
    run_simple(
        '0.0.0.0', 5000,
        app,
        use_reloader=True, use_debugger=True, threaded=True)