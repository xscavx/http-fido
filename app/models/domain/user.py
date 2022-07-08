# -*- coding: utf-8 -*-
from pydantic import BaseModel, EmailStr


class User(BaseModel):
  id: str | None = None
  email: EmailStr

  class Config:
    orm_mode = True
