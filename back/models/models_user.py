from pydantic import BaseModel, EmailStr , ValidationError
from typing import List , Optional
from fastapi.responses import FileResponse
from datetime import datetime
from enum import Enum

class New_User(BaseModel):
    name: str
    surname: str
    password: str
    email: str
    phone: int
  
class SignIn_Check(BaseModel):
    username: EmailStr
    password: str

class ConnectionHandle(BaseModel):
    handle : str
    id     : int
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    scopes: list[str] = []

class ChangeMail(BaseModel):
    new_mail : EmailStr

class ChangePasswd(BaseModel):
    new: str
    current : str
    
class UserSearchModel(BaseModel):
    query : str

class UserSearchResponse(BaseModel):
    id : int 
    name : str
    email : EmailStr
    phone : str
    avatar: str
    age: Optional[int] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None

class UserId(BaseModel):
    user_id:int

#============ARTICLES
    
class ArticleResponse(BaseModel):
    id   : int
    name : str
    surname: str
    profess : str
    art_id : int
    title: str
    uploader : int
    isInterest : Optional[bool] = None

class FriendInterestArticle(BaseModel): #If i use article : ArticleResponse , after teh query it expects data(dictionary) and another input(friend_id)
    id   : int
    name : str
    surname: str
    profess : str
    art_id : int
    title: str
    uploader : int
    friend_id : int
    isInterest : Optional[bool] = None

class CommentArticle(BaseModel):
    article_id : int
    comment : str

class FullArticleResponse(BaseModel):
    article : str
    media   : List[str]

class InterestArticle(BaseModel):
    id : int
    interest : bool
#===========================================================
#=================ADS
class ActionType(str, Enum):
    interest = "interest"
    comment = "comment"

class ArticleNotification(BaseModel):
    article_id : int
    title : str
    user_id : int
    name : str
    surname : str
    uploader : int
    action : ActionType
    time_of_action: datetime  # Timestamp of the action


class UserResponse:
    def __init__(self, user_data: dict, pictures: List[FileResponse]):
        self.user_data = user_data
        self.pictures = pictures
            
class ChatRoom(BaseModel):
    chat_id : Optional[int] = None
    user : int
    user0 : int
    message : str

class Personal_Info(BaseModel):
    profession: str
    age : Optional[int]  = None
    experience : Optional[str] = None
    education : Optional[str] = None
    skills : Optional[str] = None
    employment : Optional[str] = None
    is_age_p: bool = False
    is_experience_p: bool = False
    is_education_p: bool = False
    is_skills_p: bool = False
    is_employment_p: bool = False