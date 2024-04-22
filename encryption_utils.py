from cryptography.fernet import Fernet

# encryption_utils.py

from cryptography.fernet import InvalidToken

# Function to read symmetric encryption key from file
def read_symmetric_key(file_path):
    with open('./symmetric_key.txt', 'rb') as f:
        symmetric_key = f.read()
        # Add validation to ensure key is valid
        try:
            # Decrypt a dummy token to check if the key is valid
            Fernet(symmetric_key).decrypt(b'dummy')
        except InvalidToken:
            raise ValueError("Invalid symmetric key")
        return symmetric_key


# Function to encrypt data using a symmetric key
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data using a symmetric key
def decrypt_data(encrypted_data, key):
    print("Encrypted data:", encrypted_data)  # Print encrypted data
    print("Symmetric key:", key)  # Print symmetric key
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        print("Decrypted data:", decrypted_data)  # Print decrypted data
        decrypted_data = decrypted_data.decode()
        return decrypted_data
    except Exception as e:
        print("Error during decryption:", e)  # Print any decryption errors
        raise
