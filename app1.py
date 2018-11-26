from flask import Flask, flash
from flask import render_template
from flask import g
from flask import request, redirect
from flask_wtf import Form
from wtforms import PasswordField

#from tabel_to_dictionary import get_author
import sqlite3
app = Flask(__name__)
app.debug = True
DB_FILE = "db/test.sqlite"


def htmlify(dictionary):
    html = "<table>"
    for key, value in dictionary.items():
        html += f"<tr><td>{key}</td><td>{value}</td></tr>"
    html += "</table>"
    return html


@app.before_request
def get_db():
    db = getattr(g, "db", None)
    if db is None:
        g.db = sqlite3.connect(DB_FILE)
    return db


@app.teardown_request
def close_request(exeption):
    db = getattr(g, "db", None)
    if db:
        setattr(g, "db", None)
        db.close()


@app.route("/")
def hello():
    return personalized_hello()


@app.route("/help")
def help():
    return "no"


@app.route("/hello/<name>")
def personalized_hello(name=None): 
    return render_template("hello.html", name=name)


@app.route("/form", methods=['GET', 'POST'])
def form_demo():

    if request.method == 'POST':
        return "#offended"
        """return htmlify(request.form)"""

    return render_template("form1.html")



@app.route('/author/<author_id>', methods=['GET'])
def get_author(author_id):
    """ Getting authors from DB, into HTML """
    author = __get_author_from_db(author_id)
    return render_template("show_author.html", author=author)

""" NOT GOOD
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        return None
    else:
        flash('wrong password!')
    return None
"""

@app.route('/register')
def new_user():
   return render_template('register.html')


@app.route('/new_movie')
def new_movie():
   return render_template('new_movie.html')


@app.route('/list')
def list():
    con = sqlite3.connect("db/test.sqlite")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)
"""
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        return save_user(DB_FILE,)
"""
"""-----------------------------------------------------------------------"""
def __get_author_from_db(author_id):
    sql = """SELECT name, born, died
            FROM authors 
            WHERE id = {}""".format(author_id)

    cursor = get_db().cursor()
    cursor.execute(sql)

    result = cursor.fetchone()
    if not result:
        """ signal an error in some way """
        return None

    author = {}  # make adictionary
    author["id"] = author_id
    author["name"], author["born"], author["died"] = result

    return author

"""---------------------------NOT WORKING-------------------------"""

def __get_user_from_db(username, password):
    """ authenticate user with username and password to the database """
    cursor = get_db().cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE name = ? AND password = ?', username, password) 
    result = cursor.fetchone()
    
    if result = 0:
        msg = "Wrong username/password"
    else:
        if result > 1:                          # NOT MANDATORY IF CONSTRAINT IN DB
            msg = "Bug in the application"      # NOT MANDATORY IF CONSTRAINT IN DB
        else:                                   # NOT MANDATORY IF CONSTRAINT IN DB
            msg = None

    return msn

"""----------------------------NOT IN USE----------------------------------------"""


def save_user(db,diction):

    cursor = db.cursor()

    query = """INSERT INTO USER(name, email, password)
                VALUES("{}","{}","{}")""".format(diction["name"], diction["email"], diction["password"])

    print(query)

    cursor.execute(query)
    # IF CONSTRAINT IN DB, CHECK IF NOT ERROR OCCURED DURING THE QUERY'S EXECUTION 

    # user_id = cursor.lastrowid
    cursor.close()

    db.commit()

    return None

"""------------------------------------------------------------------------"""


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():

    if request.method == 'POST':
        try:
            name = request.form['name']
            mail = request.form['email']
            password = request.form['password']

            with sqlite3.connect("db/test.sqlite") as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO users (name,email,password)
                VALUES(?, ?, ?)""", (name, mail, password))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/add_movie', methods=['POST', 'GET'])
def add_movie():

    if request.method == 'POST':
        try:
            title = request.form['title']
            year = request.form['year']

            with sqlite3.connect("db/test.sqlite") as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO MOVIES (title,year)
                VALUES(?, ?)""", (title, year))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

"""------------------------------------------------------------------------"""

if __name__ == '__main__':
    app.run()
