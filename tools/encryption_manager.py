import os

from cryptography.fernet import Fernet
from dotenv import set_key, find_dotenv

class EncryptionManager:
    def __init__(self, applicant_key, key=None):
        # Generate a key for encryption and decryption
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
            self.applicant_key = applicant_key
            # Convert the key to a string for storing in the .env file
            self.key_str = self.key.decode()

            # Set the encryption key in the .env file
            env_path = "env"
            file_path = "env/.data"
            # Create the folder if it doesn't exist
            if not os.path.exists(env_path):
                os.makedirs(env_path)
            # Create the file if it doesn't exist
            if not os.path.exists(env_path):
                open(file_path, 'w').close()

            set_key(file_path, f"{self.applicant_key}", self.key_str)

        self.cipher_suite = Fernet(self.key)


    def encrypt_data(self, data):
        """Encrypt data."""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        """Decrypt data."""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

"""# Example usage
encryption_manager = EncryptionManager()
encrypted_text = encryption_manager.encrypt_data("Hello, world!")
print("Encrypted:", encrypted_text)

decrypted_text = encryption_manager.decrypt_data(encrypted_text)
print("Decrypted:", decrypted_text)
"""