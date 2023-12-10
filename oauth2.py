from jose import jwt, JWTError
from datetime import datetime, timedelta
import schemas
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings as sys

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key
# Algorithm
# Expiration time

SECRET_KEY = sys.secret_key
ALGORITHM = sys.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = sys.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exceptions
        print(f"The type of User ID:{user_id} is: {type(user_id)}")
        token_data = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exceptions)
