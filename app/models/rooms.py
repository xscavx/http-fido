# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Rooms(Base):
  __tablename__ = 'rooms'

  pk = Column(
    Integer,
    primary_key=True,
    index=True
  )
