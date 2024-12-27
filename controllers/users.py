from http import HTTPStatus
import os
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
import jwt
from backend.serializers.user_serializer import UserSerializer
from backend.models.user import UserModel
from backend.app import db
from backend.config.environment import SECRET

user_serializer = UserSerializer()

router = Blueprint("users", __name__)


@router.route("/signup", methods=["POST"])
def signup():
    try:
        user_dictionary = request.json
        user_model = user_serializer.load(user_dictionary)
        db.session.add(user_model)
        db.session.commit()
        return user_serializer.jsonify(user_model), HTTPStatus.OK

    except ValidationError as e:
        error = e.messages.keys()
        # mydict.keys()[mydict.values().index(16)]
        return {
            "errors": e.messages,
            "message": f"{list(e.messages.values())} {list(error)}",
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    except IntegrityError as e:
        error_info = e.orig.args
        print(error_info[0])
        if "duplicate" in error_info[0]:
            return {
                "message": "Account already exists for this email."
            }, HTTPStatus.NOT_FOUND


@router.route("/signin", methods=["POST"])
def signin():
    try:
        user_dictionary = request.json
        db_users = UserModel.query.all()
        user_found = None
        for db_user in db_users:
            if db_user.email.casefold() == user_dictionary["email"].casefold():
                user_found = db_user
        if not user_found:
            return {"messages": "User not found."}, HTTPStatus.NOT_FOUND

        if not user_found.validate_password(user_dictionary["password"]):
            return {"message": "Login failed"}, HTTPStatus.NOT_FOUND

        print("Login success!!! 🚀")
        payload = {
            "exp": datetime.now(timezone.utc) + (timedelta(days=1)),
            "iat": datetime.now(timezone.utc),
            "sub": user_found.id,
        }

        token = jwt.encode(payload, SECRET, algorithm="HS256")

        return {"message": "Log in successful 🏃‍♀️", "token": token}, HTTPStatus.OK

    except Exception as e:
        print(e)
        return {"messages": "error"}, HTTPStatus.NOT_FOUND
