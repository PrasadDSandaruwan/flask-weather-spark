from app.config.bcrypt import get_bcrypt
from app.db.userRepo import addUserRepo, getUserByEmailRepo
from flask import jsonify
from app.utility.jwt import generateToken
import re

def checkEmail(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

def checkPassword(s):
    l, u, p, d = 0, 0, 0, 0
    if (len(s) >= 8):
        for i in s:
    
            # counting lowercase alphabets
            if (i.islower()):
                l+=1           
    
            # counting uppercase alphabets
            if (i.isupper()):
                u+=1           
    
            # counting digits
            if (i.isdigit()):
                d+=1           
    
            # counting the mentioned special characters
            if(i=='@'or i=='$' or i=='_'):
                p+=1          
    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s)):
        return True
    else:
        return False


def loginService(email,password):
    print(email,password)
    user = getUserByEmailRepo(email)

    print(email+ " "+password)

    if not user:
        return jsonify({'message' : 'Invalid Login Email!'}), 401

    bcrypt = get_bcrypt()

    print(user["password"])
    print(bcrypt.generate_password_hash(password))

    if not bcrypt.check_password_hash(user["password"],password):
        return jsonify({'message' : 'Invalid Login Password!'}), 401

    token = generateToken(user)
    return jsonify({'access_token' :token}), 200 


def addUserService(first_name,last_name,email,password):    
    print("Hi")
    checkemail = checkEmail(email)
    print(checkemail)

    checkpass = checkPassword(password)
    print(checkpass)

    if not checkEmail(email):
        return "wrong email"

    if not checkPassword(password):
        return "wrong password"

    bcrypt = get_bcrypt()

    # print(""bcrypt)
    pw_hash = bcrypt.generate_password_hash(password)

    # hash_pw = generate_password_hash(password)
    print("Hashed",pw_hash)


    user_details = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": pw_hash

    }

    addUserRepo(user_details)







