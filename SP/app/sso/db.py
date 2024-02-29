from pymongo import MongoClient

from app.model import Session, User

db_config = {
    "host": "localhost",
    "port": 27017,
    "username": "root",
    "password": "example",
}

client = MongoClient(
    host=db_config["host"],
    port=db_config["port"],
    username=db_config["username"],
    password=db_config["password"],
)


async def get_session_by_id(session_id: str) -> Session:
    '''Get session from database'''
    db = client["user_db"]
    collection = db["sessions"]
    session = collection.find_one({"_id": session_id})
    # Convert session to Session model
    res = Session(**session)
    return res


async def get_session_by_user(user: User) -> Session:
    '''Get session from database'''
    db = client["user_db"]
    collection = db["sessions"]
    session = collection.find_one({"user": user.model_dump()})
    # Convert session to Session model
    res = Session(**session)
    return res


async def create_session(user: User) -> str:
    '''Create session in database'''
    db = client["user_db"]
    collection = db["sessions"]
    session = Session(user=user, created_at=0, expires_at=0)
    session_id = collection.insert_one(session.model_dump()).inserted_id
    return str(session_id)


async def delete_session_by_id(session_id: str):
    '''Delete session from database'''
    db = client["user_db"]
    collection = db["sessions"]
    collection.delete_one({"_id": session_id})


async def delete_session_by_user(user: User):
    '''Delete session from database'''
    db = client["user_db"]
    collection = db["sessions"]
    collection.delete_one({"user": user.model_dump()})
