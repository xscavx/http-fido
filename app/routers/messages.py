from fastapi import APIRouter


router = APIRouter()

@router.post('/users/{user_id}/messages')
async def create_user_message(message: str):
  return {}


@router.get('/users/{user_id}/messages')
async def list_user_messages(user_id: int):
  return {}


@router.post('/rooms/{room_id}/messages')
async def create_room_message(message: str):
  return {}


@router.get('/rooms/{room_id}/messages')
async def list_room_messages(room_id: int):
  return []
