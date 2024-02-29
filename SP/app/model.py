from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(default=None, alias="_id")
    name: str = Field(...)
    email: str = Field(...)

    def __init__(self, **data):
        self.id = data.pop("_id")
        self.name = data.pop("name")
        self.email = data.pop("email")


class Session(BaseModel):
    id: str = Field(default=None, alias="_id")
    user: User = Field(...)
    created_at: int = Field(...)
    expires_at: int = Field(...)

    def __init__(self, **data):
        self.id = data.pop("_id")
        self.user = User(**data.pop("user"))
        self.created_at = data.pop("created_at")
        self.expires_at = data.pop("expires_at")


class Entity(BaseModel):
    '''Just for mocking the business modules'''
    id: int = Field(default=None, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
