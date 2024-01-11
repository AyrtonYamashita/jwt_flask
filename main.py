from flask import Flask, request, jsonify, render_template
import jwt
import uuid
from token_creator import TokenCreator
from db_connect import Database

app = Flask(__name__)
db = Database('alt', 'postgres', 'admin', 'localhost')


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
    
    db.add_user(user_token)


    return jsonify({
        'token': user_token
    }),200


@app.route("/login", methods=["GET"])
def authorization():
    
    user = request.headers.get("username")
    password = request.headers.get("password")

    validate = db.validate_user(user, password)
    if validate["Code"] == 'E1':
        return jsonify({
            'Erro': 'Usuário inválido!'
        }), 401
    if validate["Code"] == 'E2':
        return jsonify({
            'Erro': 'Senha inválida' 
        }), 401

    return jsonify({
        'message': "Hello World!"
    }), 200
    
if __name__ == ("__main__"):
    app.run(debug=True)