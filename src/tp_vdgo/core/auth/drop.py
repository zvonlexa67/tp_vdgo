from .auth import Auth

def drop():
    auth = Auth()
    auth.drop()