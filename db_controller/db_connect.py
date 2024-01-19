import psycopg2
from token_controller.token_decode import ManageDB

token = ManageDB()

class Database:
    def __init__(self, dbname: str, user: str, password: str, host:str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.con = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        con = self.con
        cur = con.cursor()
        cur.execute("CREATE SCHEMA IF NOT EXISTS client")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client.users (
                id VARCHAR(200) PRIMARY KEY NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                senha VARCHAR(200) NOT NULL,
                permission INT NOT NULL
            )
        '''
        )
    
    def add_user(self, token_user):
        self.token_user = token_user

        user_info = token.token_validate(self.token_user)
        user = user_info["user"]
        password = user_info["pwd"]
        id = user_info["id"]
        permission = user_info["perm"]
        con = self.con
        cur = con.cursor()
        try:
            cur.execute('''INSERT INTO client.users (id, username, senha, permission) VALUES (%s, %s, %s, %s)''', (id, user, password, permission))
            con.commit()
            cur.close()
            return con
        except psycopg2.errors.UniqueViolation:
            return False

        
    def validate_user(self, user, pwd):
        self.user = user
        self.pwd = pwd
        con = self.con
        cur = con.cursor()
        cur.execute(f"SELECT * FROM client.users WHERE username= '{self.user}'")
        response_db = cur.fetchall()
        try:
            uid, username, pass_token, perm = response_db[0]
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
    
    def validate_permission(self, uid):
        self.uid = uid
        con = self.con
        cur = con.cursor()
        cur.execute(f"SELECT permission FROM client.users WHERE id= '{self.uid}'")
        perm = cur.fetchone()
        if perm[0] <=0:
            return {
                'Error': 'Usuário sem permissão',
                'Code': 'E3'
            }
        
        con.commit()
        cur.close() 
        return {
            'Sucess': 'Usuário autorizado',
            'Code': 'S2',
            'Permission': perm[0]
        } 