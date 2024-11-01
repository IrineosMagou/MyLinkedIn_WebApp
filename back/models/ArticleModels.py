#============ARTICLES
from pydantic import BaseModel
from typing import Optional , List

class ArticleResponse(BaseModel):
    id   : int
    name : str
    surname: str
    art_id : int
    title: str
    uploader : int
    category_name : str
    isInterest : Optional[bool] = None

class FriendInterestArticle(BaseModel): #If i use article : ArticleResponse , after teh query it expects data(dictionary) and another input(friend_id)
    id   : int
    name : str
    surname: str
    art_id : int
    title: str
    uploader : int
    friend_id : int
    category_name : str
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

class UpdateArticle(BaseModel):
    id : int