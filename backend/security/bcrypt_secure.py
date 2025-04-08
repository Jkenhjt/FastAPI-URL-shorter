import bcrypt

salt: bytes = b'$2b$31$5ITrP.Ugd/inl7kN.zMFh.'

def bcrypt_securing(data: str) -> str:
    return bcrypt.kdf(data.encode(), salt, 64, 100).hex()