from queries.user_queries import FIND_EMAIL_QUERY , CHANGE_EMAIL_QUERY , CHANGE_PASSWORD_QUERY , GET_PASSWORD_QUERY
from validation.passwd_hash import *
from models.models_user import ChangePasswd

class Changes():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def change_password(
            self ,
            user_id : int,
            password : ChangePasswd
    ):
        with self.db_conn as conn:
            res = conn.execute(GET_PASSWORD_QUERY , (user_id ,)).fetchone()
            if not (verify_psswd(password.current , res[0])):
                return None
            new_password = get_psswd_hash(password.new)
            conn.execute(CHANGE_PASSWORD_QUERY , (new_password , user_id))
        return {"message": "Ο κωδικός άλλαξε επιτυχώς"}
        

    def change_email(
          self , 
          user_id : int ,
          email: str
    ):
        with self.db_conn as conn:
           res = conn.execute(FIND_EMAIL_QUERY , (email , )).fetchone()    
           if res: 
               return None
           conn.execute(CHANGE_EMAIL_QUERY ,  ( email ,  user_id ))     
        return {"message": "Το ηλεκτρονικό ταχυδρομείο επιτυχώς"}
    