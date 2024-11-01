from validation.passwd_hash import *
from validation.token_val import *
from models.models_user import SignIn_Check
from queries.user_queries import SIGN_IN_CHECK_QUERY

class SignIn():
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def check_credentials(
        self ,
        cred : SignIn_Check
    ):
        with self.db_conn as conn:
            result = conn.execute(SIGN_IN_CHECK_QUERY , (cred.username,)).fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=" No User with this email")
            res = verify_psswd(cred.password , result[1])#result[1] holds the password from the previous query       
            if not res:
                raise HTTPException(status_code=400, detail="Wrong Password")
            is_admin = result[3] 
            # print(f'Elegxos an einai ontws admin {is_admin}')
            # Define scopes based on user role
            scopes = ["user"]
            if is_admin:
                scopes.append("admin")
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(data = {"sub": str(result[2]) ,"scopes": scopes}, expires_delta=access_token_expires)
        return access_token 