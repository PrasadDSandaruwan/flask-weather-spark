
from flask import current_app, g
from flask_bcrypt import Bcrypt



def get_bcrypt():
    bcrypt = getattr(g, "_bcrypt", None)
    if bcrypt is None:
        bcrypt = g._bcrypt = Bcrypt(current_app)

    return bcrypt


