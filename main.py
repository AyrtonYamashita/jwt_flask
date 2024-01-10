from flask import Flask, request, jsonify, render_template
import jwt
from datetime import datetime, timedelta
import uuid

from token_creator import TokenCreator
from db_connect import Database

app = Flask(__name__)

@app.route('/')
def teste():
    return render_template("index.html")


# Definir registro de usuário
@app.route("/create", methods=["POST"])
def authentication():

    user = request.headers.get("username")
    password = request.headers.get("password")
    id = uuid.uuid4()
    
    token = TokenCreator(user, password, id)
    user_token = token.create()
    
    db = Database('alt', 'postgres', 'admin', 'localhost')
    db.add_user(user_token)


    return jsonify({
        'token': user_token
    }),200



# Definir credencial para acesso
@app.route("/auth", methods=["GET"])
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