from backend.app import app, db
from backend.models.user import UserModel

with app.app_context():
    try:
        print("ready...")
        db.drop_all()
        db.create_all()

        users_data=[{
            "first_name": "Liv",
            "last_name" : "Darby",
            "email": "oliviadarby@live.co.uk",
            "password" : "test"
        }]

        for user_data in users_data:
            user = UserModel(**user_data)
            db.session.add(user)
        db.session.commit()

        print("Seeding some data...")
    
    except Exception as e:
        print(e)