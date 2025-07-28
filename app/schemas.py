from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel): # Define the Pydantic Post model
    title: str
    content: str
    published: bool = True  # Default value for published is True
    

class CreatePost(PostBase): 
    pass

class UserOut(BaseModel):  # This model is used for returning user data response
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True    


class Post(PostBase):  # This model is used for returning data response back to user
    id: int
    created_at: datetime
    owner_id: int  # The ID of the user who created the post
    owner: UserOut  # Include the user information who created the post by returning a pydantic model

    class Config:
        orm_mode = True

class UserCreate(BaseModel):  # Define the Pydantic User model
    email: EmailStr
    password: str


class UserLogin(BaseModel):  # Model for user login
    email: EmailStr
    password: str        

class Token(BaseModel):  # Model for the token response
    access_token: str   
    token_type: str    

class TokenData(BaseModel):  # Model for token data
    id: Optional[str] = None  # Optional user ID, can be None if not provided    