from flask import Flask, request, jsonify, render_template
import uuid
from token_controller.token_generator import TokenCreator
from token_controller.token_autorization import Auth
from token_controller.token_decode import TokenVerify
from db_controller.db_connect import Database

app = Flask(__name__)
db = Database('alt', 'postgres', 'admin', 'localhost')


@app.route('/')
def start():
    return render_template("index.html")


# Definir registro de usuário
@app.route("/create", methods=["POST"])
def create_user():
    user = request.headers.get("username")
    password = request.headers.get("password")
    id = uuid.uuid4()

    token = TokenCreator(user, password, id)
    user_token = token.create()

    db.add_user(user_token)


@app.route("/validate", methods=["GET"])
def validate_user():
    
    user = request.headers.get("username")
    password = request.headers.get("password")

    validate = db.validate_user(user, password)

    if validate["Code"] == 'E1' or validate["Code"] == 'E2':
        return jsonify({
            'Status': False
        }), 401
    
    generate_auth = Auth()
    token_auth = generate_auth.authorization(validate["Token"])

    return jsonify({
        'Status': True,
        'uid': validate["Token"],
        'Token': token_auth
    })


@app.route("/home", methods=["GET"])
def home():
    verify_token = TokenVerify()
    token_access = request.headers.get("token")
    token = verify_token.decode_token(token_access)

    
    return jsonify({
        'token': token
    })

if __name__ == ("__main__"):
    app.run(debug=True)