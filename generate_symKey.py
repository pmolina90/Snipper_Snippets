from encryption_utils import generate_symmetric_key

# Generate the symmetric encryption key
symmetric_key = generate_symmetric_key()

# Print or store the generated key securely
print("Symmetric Encryption Key:", symmetric_key)

# Optionally, you can store the key in a file
with open('symmetric_key.txt', 'wb') as key_file:
    key_file.write(symmetric_key)
