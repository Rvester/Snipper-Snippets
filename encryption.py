from config import ENCRYPTION_KEY
from cryptography.fernet import Fernet

# Ensure that the encryption key is available
if not ENCRYPTION_KEY:
    raise ValueError("No encryption key found. Please set the ENCRYPTION_KEY environment variable.")

# Initialize the Fernet cipher
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_code(code):
    """Encrypt the code snippet."""
    return cipher.encrypt(code.encode()).decode()

def decrypt_code(encrypted_code):
    """Decrypt the code snippet."""
    return cipher.decrypt(encrypted_code.encode()).decode()
