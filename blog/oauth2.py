
# aouth2 create for when user has token
# use that token for access data

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from . import schemas_d


# login url for token to access /user/login/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # error server error pata karna hai
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas_d.TokenData(email=email)

    except JWTError:
        raise credentials_exception
    #### test error
    # return token_data