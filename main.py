from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from backend.api.pydantic.model_olap import OlapUser
from backend.api.pydantic.token_model import Token
from backend.db.database import database
from backend.db.olap_service import get_frontend_fields, get_list_of_olap_tables
from backend.db.user_service import authenticate_user, create_access_token, get_current_active_user
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/olap/{olap_name}")
async def get_olap_info(olap_name):
    response = await get_frontend_fields(olap_name)
    return response


@app.get("/olap/my_tables")
async def get_my_tables():
    response = await get_list_of_olap_tables()
    return response


@app.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check() -> None:
    return


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user: OlapUser = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username, "sub_id": user.id},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=OlapUser)
async def read_users_me(current_user: OlapUser = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: OlapUser = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]
