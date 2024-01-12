import jwt
from flask import jsonify

class TokenVerify:
    def __init__(self):
        pass
    def decode_token(self, token):
        self.token = token

        if not self.token:
            return jsonify({
                'Error': "Token ausente"
            }), 400
        
        try:
            token_information = jwt.decode(token, key='exp_token', algorithms='HS256')
        except jwt.InvalidSignatureError:
            return jsonify({
                'Error': "Token inválido!"
            })
        except jwt.ExpiredSignatureError:
            return jsonify({
                'Error': "Token expirado!"
            }), 401
    
        return token_information
        



class ManageDB:
    def __init__(self):
        pass
    def token_validate(self, token_user):
        self.token = token_user
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
    
    def pass_decode(self, pwd):
        self.pass_token = pwd
        try:
            token_info = jwt.decode(self.pass_token, key='pwd_script', algorithms='HS256')
        except jwt.InvalidSignatureError:
            return jsonify({
                'Error': 'Token inválido!'
            }), 401
        except KeyError as e:
            return jsonify({
                'Error': 'Token inválido!'
            }), 401
        return token_info
            

