from cryptography.fernet import Fernet


def decrypt(data):
    if data == None:
        return
    f = Fernet(open("secret.key", "rb").read())
    code = f.decrypt(data.encode())
    print("decrypting data")
    return code.decode()

def encrypt(data):
    f = Fernet(open("secret.key", "rb").read())
    code = data.encode()
    print(code)
    print("encrypting data")
    return f.encrypt(code)


# code for deploying 
# def decrypt(data):
#     if data == None:
#         return
#     f = Fernet(open("/home/jessethommes/mysite/secret.key", "rb").read()) #TODO may need to change route to secret.key
#     print(data)
#     token = f.decrypt(data.encode())
#     return token.decode()

# def encrypt(data):
#     f = Fernet(open("/home/jessethommes/mysite/secret.key", "rb").read()) #TODO may need to change route to secret.key

#     token = f.encrypt(data.encode())
#     return (token)



#****lo
# message = "hello"
# coded = message[-2:].rjust(len(message), '*')
