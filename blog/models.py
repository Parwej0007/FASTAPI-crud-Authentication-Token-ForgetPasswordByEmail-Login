
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base_db
from sqlalchemy.types import DateTime, Boolean, Time, Interval, Date
from sqlalchemy.sql.functions import func



# user Model

class UserModel(Base_db):

    __tablename__ = "user_tb"

    id = Column(Integer, index=True, primary_key=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), default=func.now()) #last login according to sql db
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(Date(), default=func.now())

    blogs = relationship("Blog", back_populates='creator')

    # __table_args__ = {"schema": "public"}




# Blog Model

class Blog(Base_db): # Base_db is database
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True) # auto indexing id
    title = Column(String)
    body = Column(String)

    creator = relationship("UserModel", back_populates='blogs') # UserModel is class
    user_id = Column(Integer, ForeignKey("user_tb.id")) # user_tb.id table name . id

    # __table_args__ = {"schema": "public"}


# crete table for store forget password uuid key

class ForgetPasswordId(Base_db):
    __tablename__ = "forget_password"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    reset_code = Column(String)
    is_active = Column(Boolean, default=True)
    expired_in = Column(Date(), default=func.now())






