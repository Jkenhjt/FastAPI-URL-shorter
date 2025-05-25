import bcrypt

def bcrypt_securing(data: str) -> bytes:
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt(15))