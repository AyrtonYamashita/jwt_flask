import jwt
from datetime import datetime, timedelta


class Auth:
    def __init__(self):
        pass
    def authorization(self, uid):
        self.uid = uid

        token = jwt.encode({
            'uid': self.uid,
            'exp': datetime.utcnow() + timedelta(seconds=1)
        }, key='exp_token', algorithm='HS256')

        return token
