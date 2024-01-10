import psycopg2
from token_verify import InsertDB

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

        token = InsertDB(self.token_user)
        user_info = token.token_validate()
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
        