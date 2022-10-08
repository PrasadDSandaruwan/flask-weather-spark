
import imp
from app.config.bcrypt import get_bcrypt
from app.db.userRepo import addUserRepo, getUserByEmailRepo
from flask import jsonify
from app.utility.jwt import generateToken


def loginService(email,password):
    user = getUserByEmailRepo(email)

    if not user:
        return jsonify({'message' : 'Invalid Login !!'}), 401

    bcrypt = get_bcrypt()

    print(user["password"])
    print(bcrypt.generate_password_hash(password))

    if not bcrypt.check_password_hash(user["password"],password):
        return jsonify({'message' : 'Invalid Login Password !!'}), 401

    token = generateToken(user)
    return jsonify({'access_token' :token}), 200 


def addUserService(first_name,last_name,email,password):

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







