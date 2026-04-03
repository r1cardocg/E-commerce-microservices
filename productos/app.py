from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

from extensions import db, migrate
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    port = int(os.getenv('PORT', 8002))
    app.run(host='0.0.0.0', port=port, debug=True)
    