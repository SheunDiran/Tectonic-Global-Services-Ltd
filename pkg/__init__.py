from flask import Flask
from pkg import config
import os
from dotenv import load_dotenv
load_dotenv()
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

def create_app():
    from pkg.model import db
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")
    app.config.from_object(config.Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    return app

app = create_app()
from pkg import user_routes, myforms, admin_route