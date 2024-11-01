from pydantic import BaseModel 
from typing import Optional

class AdResponse(BaseModel):
    id   : int
    name : str
    surname: str
    ad_id : int
    title: str
    uploader : int
    isInterest : Optional[bool] = None

class FriendInterestAd(BaseModel):
    id   : int
    name : str
    surname: str
    ad_id : int
    title: str
    uploader : int
    friend_id : int
    isInterest : Optional[bool] = None

class FullAdResponse(BaseModel):
    ad : str
class UploadAd(BaseModel):
    title : str
    text : str
    id : Optional[int] = None
class InterestAd(BaseModel):
    id:int
    interest: bool
class CommentAd(BaseModel):
    ad_id : int
    comment: str