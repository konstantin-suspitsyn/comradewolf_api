from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from pydantic import BaseModel


class OlapTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    link_toml: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, )
    updated_at: Optional[datetime] = Field(default=None)
    database_type_id: int


class OlapUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str


class OlapUserDTO(BaseModel):
    id: int
    username: str


class UserLoginModel(BaseModel):
    username: str
    password: str


class OlapToml(BaseModel):
    id: Optional[int]
    name: str
    link_toml: str


class OlapTableResponse(BaseModel):
    id: Optional[int]
    name: str
