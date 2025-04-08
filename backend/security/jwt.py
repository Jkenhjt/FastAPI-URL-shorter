from authlib.jose import jwt


key: str = """  9c03b53595e94ce1b0573a5d0a682d4e
                df25736729f991506949bdc2681d1c43
                d785c7a21dbe531f7cf8bc4750e7e5a0
                7eafe64c95cfd061167472f669ad22c3 """


def create_token(id: int) -> str:
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "sub": id,
        "exp": -1
    }

    return jwt.encode(header=header, payload=payload, key=key, check=True).decode()