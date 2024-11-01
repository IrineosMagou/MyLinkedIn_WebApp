from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")


def get_psswd_hash(psswd):
    return pwd_context.hash(psswd)

def verify_psswd(plain , hashed):
    return pwd_context.verify(plain , hashed)