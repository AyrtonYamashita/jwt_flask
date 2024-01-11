import psycopg2
from token_verify import ManageDB
from flask import jsonify

token = ManageDB()

class Database:
    def __init__(self, dbname: str, user: str, password: str, host:str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.con = psycopg2.connect(
        dbname = self.dbname,
        user = self.user,
        password = self.password,
        host = self.host
    )

    def add_user(self, token_user):
        self.token_user = token_user

        user_info = token.token_validate(self.token_user)
        user = user_info["user"]
        password = user_info["pwd"]
        id = user_info["id"]

        con = self.con
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS email_alt.usuarios (
                id VARCHAR(200) PRIMARY KEY NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                senha VARCHAR(200) NOT NULL
            )
        '''
        )
        cur.execute('''INSERT INTO email_alt.usuarios (id, username, senha) VALUES (%s, %s, %s)''', (id, user, password))
        con.commit()
        cur.close()

        return con
        
    def validate_user(self, user, pwd):
        self.user = user
        self.pwd = pwd
        con = self.con
        cur = con.cursor()
        cur.execute(f"SELECT * FROM email_alt.usuarios WHERE username= '{self.user}'")
        response_db = cur.fetchall()
        try:
            uid, username, pass_token = response_db[0]
        except IndexError:
            return {
                'Error': 'Usuário inválido',
                'Code': 'E1'
            }
        pwd_decode = token.pass_decode(pass_token)
        if self.pwd != pwd_decode["pwd"]:
            return {
                'Error': 'Senha inválida',
                'Code': 'E2'
            }
            
        return {
            'Success': 'Autenticado com sucesso',
            'Code': 'S1',
            'Token': uid
        }
        