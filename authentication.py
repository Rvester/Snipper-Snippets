import bcrypt

def hash_password(password: str) -> bytes:
    """Hash the user's password with a salt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode(), hashed)
