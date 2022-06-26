from fastapi import APIRouter


router = APIRouter(
  prefix='/rooms'
)

@router.post('/')
async def create_room():
  return {}


@router.get('/')
async def list_all_rooms():
  return []


@router.get('/{room_id}')
async def get_room(room_id: int):
  return {}


@router.get('/{room_id}/users')
async def list_room_users(room_id: int):
  return []
