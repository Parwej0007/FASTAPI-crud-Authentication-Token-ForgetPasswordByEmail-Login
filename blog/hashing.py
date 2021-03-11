# for hash password
from passlib.context import CryptContext




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class for calling for hash password
class HashPassword():
    def bcrypt(password: str):
        return pwd_context.hash(password) # call pwd_context

    def verify_pass(plan_password, hashed_password):
        return pwd_context.verify(plan_password, hashed_password)
