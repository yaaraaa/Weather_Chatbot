from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from Backend.api import all_routes


def create_app():
    """Creates and configures the Flask application with all API blueprints."""
    app = Flask(__name__)
    for bp in all_routes:
        app.register_blueprint(bp, url_prefix="/api")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
