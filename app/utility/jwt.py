import os
import jwt
from datetime import datetime, timedelta
from flask import current_app,request,jsonify

import configparser
from functools import wraps

from app.db.userRepo import getUserByEmailRepo

config = configparser.ConfigParser()

config.read(os.path.abspath(os.path.join(".ini")))

def generateToken(user):
    token = jwt.encode({
            'first_name': user["first_name"],
            'last_name' : user["last_name"],
            "email":user["email"],
            "exp":datetime.utcnow() + timedelta(minutes = int(config["TOKEN"]["EXP_MIN"]))
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    return token

def authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])


            email = data["email"]
            user = getUserByEmailRepo("s")
 
            if not user:
                return jsonify({'message' : 'Invalid Token !!'}), 401

        except Exception as e:
            return jsonify({
                'message' : "Invalid Token !!"
            }), 401

        return  f(*args, **kwargs)
  
    return decorated

