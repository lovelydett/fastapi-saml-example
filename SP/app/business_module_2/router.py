from fastapi import FastAPI, Depends

from app.model import Entity, User
from app.sso.helper import get_current_user

api = FastAPI(prefix="/api/v1/module2")


@api.get("entities")
async def get_entities(user: User = Depends(get_current_user)):
    entities = [
        {"id": 1, "name": "Entity 1", "description": "This is entity 1"},
        {"id": 2, "name": "Entity 2", "description": "This is entity 2"},
    ]
    return 200, entities


@api.get("entities/{entity_id}")
async def get_entity(entity_id: int, user: User = Depends(get_current_user)):
    entity = {"id": entity_id, "name": "Entity 1",
              "description": "This is entity 1"}
    return 200, entity


@api.post("entities")
async def create_entity(entity: Entity, user: User = Depends(get_current_user)):
    return 200, {"message": "Entity created"}
