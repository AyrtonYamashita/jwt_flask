import jwt
from datetime import datetime, timedelta

class TokenCreator:
    def __init__(self, user, password, id, permission):
        self.user = user
        self.password = password
        self.id = id
        self.permission = permission
    
    def create(self):
        pass_crypt = jwt.encode({
            'pwd': self.password
        }, key='pwd_script', algorithm='HS256')

        token = jwt.encode({
            'user': self.user,
            'pwd': pass_crypt,
            'id': str(self.id),
            'perm': int(self.permission),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, key='1234', algorithm='HS256')
        return token