# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users(Base):
  __tablename__ = 'users'

  pk = Column(
    Integer,
    primary_key=True,
    index=True
  )
  email = Column(
    String,
    nullable=False,
    index=True
  )
