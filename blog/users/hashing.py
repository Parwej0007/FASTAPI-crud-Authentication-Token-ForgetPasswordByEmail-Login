# hashing the password
from passlib.context import CryptContext




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# after hashing we return
class Hashing:
    def bcrypt_pass(password: str):
        return pwd_context.hash(password)