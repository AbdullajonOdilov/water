from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hasher(password):
    return pwd_context.hash(password)
def tekshiradi(kiritilgan_password,  bazadagi_password):
    return pwd_context.verify(kiritilgan_password,bazadagi_password)
