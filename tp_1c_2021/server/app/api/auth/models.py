import enum

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db


class RoleName(enum.Enum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    profile_pic = db.Column(db.String, nullable=False)
    roles = relationship("UserRole", back_populates="user")

    # token = relationship("Token", back_populates="user")

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @hybrid_property
    def role_names(self):
        return [role.role_name.name for role in self.roles]


class UserRole(db.Model):
    email = db.Column(db.String, ForeignKey(User.email), primary_key=True)
    role_name = db.Column(db.Enum(RoleName), nullable=False, default=RoleName.USER)
    user = relationship("User", uselist=False, back_populates="roles")

    def __init__(self, user):
        self.email = user.email


class WhitelistedUser(db.Model):
    email = db.Column(db.String, primary_key=True)

    def __init__(self, email):
        self.email = email

# class Token(db.Model):
#    access_token = db.Column(db.String(), primary_key=True)
#    email = db.Column(db.String, ForeignKey(User.email), primary_key=True)
#    user = relationship("User", uselist=False, back_populates="token")
