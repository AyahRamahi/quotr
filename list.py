# a program that lists all quotes and their authors in my database

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import csv

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main ():
    quotes = db.execute("SELECT * from quotes").fetchall()
    for q in quotes:
        print(f"{q[0]} by {q[2]}")

if __name__ == '__main__':
    main()