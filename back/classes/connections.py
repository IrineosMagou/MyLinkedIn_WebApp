from queries.user_queries import NEW_CONNECTION , ACCEPT_REQUEST , DECLINE_REQUEST , CANCEL_REQUEST
from datetime import datetime
from fastapi import HTTPException

class Connections():
    def __init__(self , db_conn):
        self.db_conn = db_conn

    def connection_request(
            self ,
            id : int ,
            user_id : int 
    ):
        ts = datetime.utcnow()
        try:
            with self.db_conn as conn:
                conn.execute(NEW_CONNECTION , (id , user_id, ts ))
            return{"Message" : "Αναμονή για αποδοχή αιτήματος"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def handle_request(
            self , 
            id : int , 
            user_id : int ,
            handle : str
    ):
        ts = datetime.utcnow()
        try:
            with self.db_conn as conn:
                if handle == 'ACCEPT':
                    conn.execute(ACCEPT_REQUEST , (ts , user_id , id))
                    return{"Message" : "Επιτύχια Σύνδεσης"}
                elif handle == 'REJECT':
                    conn.execute(DECLINE_REQUEST , (ts , user_id , id))
                    return{"Message" : "Επιτυχής Απόριψη Σύνδεσης"}
                else :
                    conn.execute(CANCEL_REQUEST , (user_id , id))
                    return{"Message" : "Επιτυχία"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    