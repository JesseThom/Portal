from cryptography.fernet import Fernet


def decrypt(data):
    print(data)
    if data == None:
        return
    f = Fernet(open("secret.key", "rb").read())
    code = f.decrypt(data)
    print("decrypting data")
    return code.decode()

def encrypt(data):
    f = Fernet(open("secret.key", "rb").read())
    code = data.encode()
    print("encrpting data")
    return f.encrypt(code)


#****lo
# message = "hello"
# coded = message[-2:].rjust(len(message), '*')
