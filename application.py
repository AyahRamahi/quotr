from flask import Flask,render_template,request,session,flash,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import random
#local imports
from database import create_users_db,register_user,username_exist,login_user

#create users database if not exists
create_users_db()

# making a flask app
app = Flask(__name__)
# configure app before passing it to session
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
Session(app)
# setting up SQLAlcehmy engine
# an engine is an object created by SQLAlchemy to take care of interacting with the database
engine = create_engine(os.getenv("postgres://vjdmhspaeeftpn:ab231d6947725943e650f2f443637430a643f62292e00b39f9d4eb984f4a53ab@ec2-54-221-237-246.compute-1.amazonaws.com:5432/d9jrqdh13jlpkn
"))
# creates different sessions for different users
db = scoped_session(sessionmaker(bind=engine))

app.secret_key = os.urandom(24)

#number of quotes on database
quotes_number=db.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]

@app.route("/")
def index():
    # shows a random quote from the database with its author and username who submitted it
    quote_id = random.randint(1,quotes_number)
    q = db.execute("SELECT * FROM quotes WHERE id = :id",{'id':quote_id}).fetchone()
    user = db.execute("SELECT * FROM users WHERE user_id = :user_id",{'user_id':q[3]}).fetchone()
    user=user[1]
    return render_template("index.html",quote=q[1],author=q[2],user=user)

@app.route("/addQuote",methods=["GET","POST"])
def addQuote ():
    global quotes_number

    # adds quote to the database with the user_id
    try:
        session['logged_in']
    except KeyError:
        session['logged_in'] = False
    if not session['logged_in'] :
        return redirect(url_for("login"))
    else :
        if request.method == "GET":
            return render_template("addQuote.html")
        elif request.method == "POST" :
            quote = request.form['quote']
            author = request.form['author']
            user_id = session['user_id']
            db.execute("INSERT INTO quotes (quote,author,user_id) VALUES (:quote,:author,:user_id)"
            ,{'quote':quote,'author':author,'user_id':user_id})
            db.commit()
            quotes_number +=1
            return redirect(url_for("main"))

@app.route("/delete/<int:quoteID>")
def delete(quoteID):
    global quotes_number

    # deletes a quote from the quotes the user submitted before
    try:
        session['logged_in']
    except KeyError:
        session['logged_in'] = False
    if not session['logged_in'] :
        return redirect(url_for("login"))
    else :
        db.execute("DELETE FROM quotes WHERE id = :id",{'id':quoteID})
        db.commit()
        quotes_number -=1
        return redirect(url_for("main"))

@app.route("/main")
def main():
    global quotes_number

    # shows the quotes that this user submitted
    try :
        session["logged_in"]
    except KeyError :
        session["logged_in"] = False
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else :
        print(quotes_number)
        user_quotes = db.execute("SELECT * FROM quotes WHERE user_id = :user_id"
        ,{'user_id':session['user_id']}).fetchall()
        return render_template("main.html",user_quotes=user_quotes)

@app.route("/login",methods=["POST","GET"])
def login():
    # login page
    try:
        session["logged_in"]
    except KeyError:
        session["logged_in"] = False
    print(session['logged_in'])
    if not session["logged_in"] :
        if request.method == "GET":
            return render_template("login.html",error=False)
        else :
            usr = request.form['username']
            pas = request.form['password']
            check = login_user(usr,pas)
            if check == False :
                return render_template("login.html",error=True)
            elif request.method == "POST" :
                session["logged_in"] = True
                session['user_id'] = check[0]
                return redirect(url_for("main"))
    else :
        return redirect(url_for("main"))

@app.route("/logout")
def logout():
    # logs user out
    session["logged_in"] = False
    del session['user_id']
    return redirect(url_for("index"))

@app.route("/signup",methods=["POST","GET"])
def signup():
    # signup page
    try :
        session["logged_in"]
    except KeyError:
        session["logged_in"] = False
    if not session["logged_in"]:
        if request.method == "GET":
            return render_template("signup.html",error=False)
        else :
            usr = request.form['username']
            pas = request.form['password']
            if username_exist(usr):
                return render_template("signup.html",error=True)
            else :
                register_user(usr,pas)
                return redirect(url_for("login"))
    else :
        return redirect(url_for("main"))
