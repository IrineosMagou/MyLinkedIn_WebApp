from queries.user_queries import SEARCH_USERS , CONNECTED_USER_FULL_VIEW , GET_CONNECTION_STATUS , GET_CONNECTIONS , IS_USER_CONNECTED , NOT_CONNECTED_USER_FULL_VIEW
from models.models_user import UserSearchModel , UserSearchResponse
from typing import Tuple , Any

class UserSearch():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    @classmethod
    def _create_model_from_tuple (cls , row : Tuple[Any])-> UserSearchResponse:
        return UserSearchResponse(
            id = row[0] ,
            name = row[1] ,
            email = row[2] ,
            phone = row[3] , 
            avatar = row[4] ,
        )
    def connections_of_user(
            self ,
            id : int
    ):
        with self.db_conn as conn:
            results = conn.execute(GET_CONNECTIONS , (id ,id,id )).fetchall()
        if not results:
            return None
        return [
            self._create_model_from_tuple(row)
            for row in results
        ]
    

    def search_user(
            self , 
            profess : UserSearchModel ,
            id : int
    ):
        with self.db_conn as conn:
            res = conn.execute(SEARCH_USERS , (profess.query , id )).fetchall()
            if not res:
                return None
        return [
            self._create_model_from_tuple(row)
            for row in res
        ]
    
    def user_view(
        self , 
        id : int , 
        user_id : int
    ):
        with self.db_conn as conn:
            # result = None
            res = conn.execute(IS_USER_CONNECTED,(id , user_id , user_id , id)).fetchone()
            if res:#they are connected , so return the full user info
                result = conn.execute(CONNECTED_USER_FULL_VIEW , (user_id, )).fetchone()
            else :
                result = conn.execute(NOT_CONNECTED_USER_FULL_VIEW , (user_id, )).fetchone()

            if not result:
                return None
            columns = ["id" , "name" , "surname" , "profession" , "email" , "phone" , "avatar" , "age" , "experience" , "education" , "skills"]
            user_dict = dict(zip(columns, result))
            res = conn.execute(GET_CONNECTION_STATUS , (id , user_id , user_id , id)).fetchone()#Check if there is a connection pending , or rejected
            if res:
                if(res[1] == id):#current_user is the sender
                        user_dict['sender'] = 1
                else:
                        user_dict['sender'] = 0
                if res[0] == 'Pending':
                    user_dict['connection_status'] = 'Pending'
                elif res[0] == 'Accepted':
                    user_dict['connection_status'] = 'Accepted'
               
            # print(user_dict)   
        return{"data" : user_dict}
    

            


            