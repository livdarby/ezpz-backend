from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from backend.serializers.user_serializer import UserSerializer
from flask import Blueprint, request
from marshmallow import ValidationError
from backend.app import db

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
        print(e)
        return {
            "errors": e.messages,
            "message": "Something went wrong",
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    except IntegrityError as e:
        error_info = e.orig.args
        print(error_info[0])
        if "duplicate" in error_info[0]:
            return {"message": "Account already exists for this email."}
