from models.models_user import UserSearchResponse , ArticleNotification
from queries.user_queries import PENDING_CONNECTIONS , ARTICLES_INTERACT
from typing import Tuple , Any

class UserAccount():
    def __init__(self , db_conn):
        self.db_conn = db_conn

    @classmethod
    def _create_model_from_tuple (cls , row : Tuple[Any])-> UserSearchResponse:
        return UserSearchResponse(
            id = row[0] ,
            name = row[1] ,
            email = row[2] ,
            phone = row[3] , 
            avatar = row[4]
        )
    
    @classmethod
    def _create_model_from_tuple0(cls , row : Tuple[Any])-> ArticleNotification:
        return ArticleNotification(
            article_id = row[0] ,
            title = row[1] ,
            user_id = row[2] ,
            name = row[3] , 
            surname = row[4] ,
            uploader = row[5],
            action = row[6],
            time_of_action = row[7]
        )
    
    def notifications(
            self ,
            id : int
    ):
            with self.db_conn as conn:
                result = conn.execute(PENDING_CONNECTIONS , (id , )).fetchall()
                res = conn.execute(ARTICLES_INTERACT , (id ,id)).fetchall()
                if not (result or res):
                     return None
            return {
                "pending_connections": [
                    self._create_model_from_tuple(row) for row in result
                ],
                "article_interactions": [
                    self._create_model_from_tuple0(row) for row in res
                ]
                }
    