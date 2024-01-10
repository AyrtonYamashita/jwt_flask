from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Definir registro de usuário
@app.route("/create", methods=["POST"])
def authentication():
    user = request.headers.get("username")
    password = request.headers.get("password")
    id = uuid.uuid4()
    
    token = jwt.encode({
        'user': user,
        'pwd': password,
        'id': str(id)
    }, key='1234', algorithm='HS256')
    
    return jsonify({
        'token': token
    }), 200
    

# Definir credencial para acesso
@app.route("/home", methods=["GET"])
def authorization():
    
    raw_token = request.headers.get("Authorization")
    user = request.headers.get("username")
    password = request.headers.get("password")
    
    if not raw_token:
        return jsonify({
            'Error': "Acesso negado!"
        }), 400
        
    try:
        token = raw_token.split()[1]
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
        
    if user != user_token:
        return jsonify({
            "Error": "Usuário inválido!"
        }), 401
        
    if password != pwd_token:
        return jsonify({
            "Error": "Senha inválida!"
        })

    return jsonify({
        'message': "Hello World!"
    }), 200
    
if __name__ == ("__main__"):
    app.run(debug=True)