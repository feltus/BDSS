from flask.ext.login import UserMixin
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import backref, relationship

from .common import BaseModel

class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    ## @var id
    #  Unique ID for this user.
    id = Column(Integer(), primary_key=True, nullable=False)

    ## @var name
    #  User's full name.
    name = Column(String(100), nullable=False)

    ## @var email
    #  User's email address.
    email = Column(String(50), nullable=False, unique=True)

    ## @var password_hash
    password_hash = Column(String(80), nullable=False)

    ## @var jobs
    #  Jobs this user has submitted.
    jobs = relationship('Job', backref='owner')

    ## @var keys
    #  SSH keys owned by this user.
    keys = relationship('SSHKey', backref='owner')
