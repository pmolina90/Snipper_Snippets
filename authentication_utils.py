import bcrypt

def hash_password(password):
    #add salt and hash to the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(input_password, hashed_password):
    #verify imput password against hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))