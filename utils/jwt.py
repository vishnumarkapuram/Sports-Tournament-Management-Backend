from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "a7Dk9Qw2Zx5Lp8Mn3Vt6Hs1Jr4Cy0FbE"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None