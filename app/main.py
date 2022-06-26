
from fastapi import FastAPI

from app.routers import messages, rooms, users


app = FastAPI(title='Test')
app.include_router(messages.router)
app.include_router(rooms.router)
app.include_router(users.router)
