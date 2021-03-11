from pydantic import BaseModel
from typing import List, Optional




# validate create blog by client use pydantic
class BlogCreate(BaseModel):
    title: str
    body: str

# This is using for response some column(data) to user eg= only want to show title not body
# show only two title or body when inherit BlogCreate(Parent)
# for only title inherit BaseModel and define title
class BlogCreateResponse(BaseModel):
    title: str
    # for getting pydantic orm otherwise will get server error
    class Config():
        orm_mode = True


# create pydantic model for user (validate data)

# class BlogUser(BaseModel):
#     name: str
#     email: str
#     password: str
#
# class BlogUserResponseModel(BaseModel):
#     name: str
#     email: str
#
#     class Config():
#         orm_mode = True


class CreateUserSchema(BaseModel):
    username:  str
    email: str
    first_name: str
    last_name: str
    password1: str
    password2: str

class ListSchemaUser(BaseModel):
    username: str
    email: str
    # is_active: bool

    class Config():
        orm_mode = True



class ShowBlog(BaseModel):
    title: str
    body: str
    owner: ListSchemaUser
    # when show blog also user will show

    class Config():
        orm_mode = True


################login

class LoginSchema(BaseModel):
    email: str
    password: str


################## token #############

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# Forget password
class UserPassForgetSchema(BaseModel):
    email: str