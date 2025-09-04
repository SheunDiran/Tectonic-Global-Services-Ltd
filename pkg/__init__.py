from flask import Flask
import os
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

def create_app():
    from pkg.model import db
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()
from pkg import user_routes, admin_route
