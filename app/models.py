from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.model, UserMixin):
    id = db.column(db.integer, primary_key=True)
    name = db.column(db.string(100), nullable=False)
    employee_number = db.column(db.integer, nullable=False, unique=True)
    hashed_password = db.column(db.string(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
