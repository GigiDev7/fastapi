from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


def compare_passwords(password: str, hashedPassword: str):
    return pwd_context.verify(password, hashedPassword)
