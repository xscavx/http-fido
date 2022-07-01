# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.database import create_tables
from app.routers import access, messages, rooms, users


app = FastAPI(title='Test')

@app.on_event('startup')
async def initialize_db():
  await create_tables()

app.include_router(access.router)
app.include_router(messages.router)
#app.include_router(rooms.router)
app.include_router(users.router)
