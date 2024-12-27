from sqlalchemy.ext.hybrid import hybrid_property
from backend.app import db, bcrypt


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, unique=False, nullable=False)
    last_name = db.Column(db.Text, unique=False, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=True)

    @hybrid_property
    def password(self):
        pass

    @password.setter
    def password(self, password_plaintext):
        encoded_hashed_pw = bcrypt.generate_password_hash(password_plaintext)
        self.password_hash = encoded_hashed_pw.decode("utf-8")
    
    def validate_password(self, login_password):
        return bcrypt.check_password_hash(self.password_hash, login_password)