from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def create_users_db ():
    columns = """
        user_id SERIAL PRIMARY KEY,
        username VARCHAR UNIQUE,
        password VARCHAR
    """
    db.execute(f"CREATE TABLE IF NOT EXISTS users ({columns})")
    db.commit()

def register_user(username,password):
    db.execute("INSERT INTO users (username,password) VALUES (:username,:password)"
    ,{'username':username,'password':password})
    db.commit()
    print("registered new user!")

def username_exist (username):
    lst = db.execute("SELECT * FROM users WHERE username = :username",{'username':username}).fetchall()
    if lst :
        print("username exists")
        return True
    print("username doesn't exist")
    return False

def login_user (username,password):
    lst=db.execute("SELECT * FROM users WHERE username = :username",{'username':username}).fetchall()
    if lst:
        for l in lst :
            if password == l[2]:
                print("right log in data")
                return l
            break
    print("false log in data")
    return False
