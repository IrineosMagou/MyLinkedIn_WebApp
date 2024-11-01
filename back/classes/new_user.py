from models.models_user import New_User 
from validation.passwd_hash import *
from validation.token_val import *
from typing import Tuple , Any 
from fastapi import UploadFile
import os

class NewUser():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    @classmethod
    def create_tuple_from_model(
        cls ,
        new_user : New_User , 
    ) -> Tuple[Any]:
        return(
             new_user.name ,
             new_user.surname,
             new_user.password ,
             new_user.email ,
             new_user.phone 
        )
    @classmethod
    def create_model_from_tuple (cls , row : Tuple[Any])-> New_User:
        return New_User(
            name = row[0] ,
            surname = row[1] ,
            password = row[3] ,
            email = row[4] ,
            phone = row[5]
        )

    
    def create_user(
            self ,
            new_user : New_User
    ):
        with self.db_conn as conn:
            res = conn.execute(
                """ SELECT * FROM users WHERE email = ? """ , (new_user.email,)).fetchone()
            if res:
                return None
            new_user.password = get_psswd_hash(new_user.password)
            conn.execute(
                """INSERT INTO users VALUES(NULL , ? , ? , ? , ? , 0, ?  )""" ,   self.create_tuple_from_model(new_user)

            )
            new_user_id = conn.execute(
                """SELECT last_insert_rowid() FROM users"""
            ).fetchone()
            # print(f'This is the new user id =================={new_user_id}')
            scopes = ["user"]
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(data = {"sub": str(new_user_id[0]) , "scopes": scopes}, expires_delta=access_token_expires)
            return access_token
        

    def profile_picture(
            self ,
            picture : Optional[UploadFile] = None,
            user : Optional[int] = None
    ):
        if picture:
            pic_dir = "/mnt/c/Users/User/Desktop/TED24/201700208_ΤΕΔ24/pictures"
            path_to_save = '/pictures/'
            if not user:
                with self.db_conn as conn:
                    new_user = conn.execute(
                    """SELECT last_insert_rowid() FROM users"""
                ).fetchone()
                    user = new_user[0]
            pic_name = f"{str(user)}.jpg"
            pic_path = os.path.join(pic_dir , pic_name)
            with open(pic_path, "wb") as writer:
                writer.write(picture.file.read())
            path_to_send = path_to_save + pic_name
            with self.db_conn as conn:
                 conn.execute("""INSERT INTO user_picture
                                VALUES (? , ?)
                                """ , (user ,path_to_send ))