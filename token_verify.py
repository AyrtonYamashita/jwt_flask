import jwt
from flask import jsonify

class TokenVerify:
    def __init__(self, token, user, password):
        self.token = token
        self.user = user
        self.password = password
    def validate(self):

        if not self.token:
            return jsonify({
                'Error': "Acesso negado!"
            }), 400
        try:
            token = self.token.split()[1]
            token_information = jwt.decode(token, key='1234', algorithms='HS256')
            user_token = token_information["user"]
            pwd_token = token_information["pwd"]
        except jwt.InvalidSignatureError:
            return jsonify({
                'Error': "Token inválido!"
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'Error': "Token expirado!"
            }), 401
        
        if self.user != user_token:
            return jsonify({
                    "Error": "Usuário inválido!"
                }), 401
        if self.password != pwd_token:
            return jsonify({
                "Error": "Senha inválida!"
            })

class InsertDB:
    def __init__(self, token_user):
        self.token = token_user

    def token_validate(self):
        try:
            token_info = jwt.decode(self.token, key='1234', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return jsonify({
                'Error': "Token Expirado!"
            }), 401
        except jwt.InvalidSignatureError:
            return jsonify({
                'Error': 'Token Inválido!'
            }), 401

        return token_info

