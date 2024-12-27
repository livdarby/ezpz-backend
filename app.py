from http import HTTPStatus
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config.environment import db_URI

app = Flask(__name__)

bcrypt = Bcrypt(app)

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World 🌍", HTTPStatus.OK

app.config["SQLALCHEMY_DATABASE_URI"] = db_URI

CORS(app)

db = SQLAlchemy(app)

marsh = Marshmallow(app)

from backend.controllers import users

app.register_blueprint(users.router, url_prefix="/api")

