from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.api.pydantic.token_model import TokenData
from backend.db.database import database

from backend.api.pydantic.model_olap import OlapUser
from settings import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

sql_get_user = """
SELECT id, username, "password", email
FROM cwb."user"
WHERE cwb."user".username = '{}';
"""

sql_get_user_by_id = """
SELECT id, username, "password", email
FROM cwb."user"
WHERE cwb."user".id = {};
"""


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the password matches the stored password.
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_name(username: str) -> OlapUser:
    result = await database.fetch_one(sql_get_user.format(username))
    user = OlapUser(id=result["id"], username=result["username"], email=result["email"], password=result["password"])
    return user


async def get_user_by_id(user_id: int) -> OlapUser:
    result = await database.fetch_one(sql_get_user_by_id.format(user_id))
    user = OlapUser(id=result["id"], username=result["username"], email=result["email"], password=result["password"])
    return user


async def authenticate_user(username: str, password: str) -> OlapUser | bool:
    user = await get_user_by_name(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("sub_id")
        if username is None:
            raise credential_exception

        if user_id is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = await get_user_by_name(username=token_data.username)
    if user is None:
        raise credential_exception

    return user


def create_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_active_user(current_user: OlapUser = Depends(get_current_user)):
    return current_user
