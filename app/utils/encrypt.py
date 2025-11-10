# util for encryption and stuff
import bcrypt

# returns hashed password
def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return [hashed_password]

# password_input is inputed password, password is actual user password
def check_password(password_input: bytes, password: bytes) -> bool:
    return bcrypt.checkpw(password_input, password)

