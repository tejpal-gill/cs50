#Assembing all the requirements
import json
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

#Configuring the application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///insight.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#Defining the necessary functions

#this function was taken from helpers.py provided in pset9 finance
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    return render_template("apology.html", code=code, message=message), code

# Page not found (404)
@app.errorhandler(404)
def page_not_found(e):
    return apology("Page not found", 404)

#index page
@app.route("/")
@login_required
def index():
    id = session["user_id"]
    query = ''' SELECT
        s.FirstName || ' ' || s.LastName || ' ' || c.ClassName || ' (' || s.Rollno || ')' AS Name,
        ROUND(AVG(m.ObtainedMarks), 2) AS Marks,
        MAX(m.ObtainedMarks) - MIN(m.ObtainedMarks) AS Spread
        FROM Marks m
        JOIN Students s ON m.StudentID = s.StudentID
        JOIN Classes c ON s.ClassID = c.ClassID
        JOIN Tests t ON m.TestID = t.TestID
        WHERE t.id = ? GROUP BY Name;'''

    # Fetch data from the database
    result = db.execute(query, id)

    # Convert data to a list of dictionaries while iterating over the result set
    result = [{'Name': row['Name'], 'Marks': row['Marks'],'Spread': row['Spread']} for row in result]

    # Return JSON response for AJAX requests
    if request.is_json:
        return jsonify(result)

    return render_template("index.html", data=json.dumps(result))

# /students
@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    id = session["user_id"]
    classes = db.execute("SELECT * FROM classes")
    rollno_q = "SELECT Rollno FROM students where ClassID = ?"
    data = db.execute("SELECT Students.*, Classes.ClassName FROM Students JOIN Classes ON Students.ClassID = Classes.ClassID WHERE id = ? ORDER BY StudentId DESC;", id)
    if request.method == "GET":
        return render_template("students.html", classes=classes, data=data)
    # Retriving values from Form
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    grade = int(request.form.get("grade"))
    rolln = request.form.get("rolln")
    rolls = db.execute(rollno_q, grade)
    # Validating inputs
    if not fname:
        return apology("Must provide First Name")
    elif not lname:
        return apology("Must provide Last Name")
    elif grade not in [grade["ClassID"] for grade in classes]:
        return apology("FBI, Openup!")
    elif rolln.isdigit() == False:
        return apology("Must provide Rollno")
    elif int(rolln) > 999 or int(rolln) < 0:
        return apology("FBI, Openup!")
    elif int(rolln) in [roll["Rollno"] for roll in rolls]:
        return apology("Rollno already assigned")
    # Regisering Student into the database
    cmd = "INSERT INTO Students (id, FirstName, LastName, ClassID, Rollno) VALUES (?, ?, ?, ?, ?)"
    db.execute( cmd, id, fname, lname, grade, int(rolln))
    return redirect("#")

# /tests
@app.route("/tests", methods=["GET", "POST"])
@login_required
def tests():
    id = session["user_id"]
    classes = db.execute("select * from classes")
    subjects = db.execute("select * from subjects")
    dq = "select * FROM students where ClassID= ? ORDER BY Rollno"
    tst = """SELECT Tests.*, Classes.ClassName, Subjects.SubjectName FROM Tests JOIN Classes ON Tests.ClassID = Classes.ClassID
        JOIN Subjects ON Tests.SubjectID = Subjects.SubjectID WHERE Tests.id = ? ORDER BY Tests.TestID DESC;"""

    # Displaying Form 1
    if request.method == "GET":
        tests = db.execute(tst, id)
        return render_template("test1.html",  classes=classes, subjects=subjects, tests=tests)

    # Getting test details
    if 'form1_submit' in request.form:
        test = str(request.form.get("testname"))
        date = request.form.get("date")
        gra = int(request.form.get("grade"))
        sub = int(request.form.get("subject"))
        # Validating user in puts
        if not test:
            return apology("Must provide Test Name")
        elif not date:
            return apology("Must provide Date")
        elif gra not in [grade["ClassID"] for grade in classes]:
            return apology("FBI, Openup!")
        elif sub not in [subject["SubjectID"] for subject in subjects]:
            return apology("FBI, Openup!")
        db.execute("INSERT INTO Tests (TestName,SubjectID,ClassID, id, date) VALUES (?,?,?,?,?)", test, sub, gra, id, date)
        testdb = db.execute("SELECT * FROM Tests WHERE TestName = ?", test)
        data = db.execute(dq, gra)
        return render_template("test2.html", data=data, grade=gra, test=testdb[0]["TestID"])

    # Inputting the grades for each student in that class
    data = data = db.execute(dq, request.form.get("grade"))
    test = db.execute("SELECT * FROM Tests WHERE TestId = ?", request.form.get("test"))
    marks = request.form.getlist("marks")
    query = "INSERT INTO marks (StudentID,TestID,ObtainedMarks) VALUES (?,?,?)"
    print(data, test, marks)
    for row in data:
        print (row)
        student_id = row['StudentID']
        test_id = test[0]['TestID']
        obtained_marks = marks.pop(0) if marks else None
        db.execute(query, student_id, test_id, obtained_marks)
    flash("Test recorded successfully.")
    return redirect("tests")

# /analyse
@app.route("/analyse",  methods=["GET", "POST"])
@login_required
def analyse():
    id = session["user_id"]
    query = ''' SELECT
        s.FirstName || ' ' || s.LastName || ' (' || s.Rollno || ')' AS Name,
        m.ObtainedMarks AS Marks,
        t.TestID AS TestID, t.TestName AS TestName,
        ROUND(m.ObtainedMarks - AVG(m.ObtainedMarks) OVER (PARTITION BY s.StudentID), 2)
        AS Average FROM Marks m
        JOIN Students s ON m.StudentID = s.StudentID
        JOIN Tests t ON m.TestID = t.TestID
        WHERE
        t.id = ? AND t.ClassID = ? AND t.SubjectID = ?;'''
    classes = db.execute("select * from classes")
    subjects = db.execute("select * from subjects")
    if request.method == "GET":
        return render_template("analyse.html",  classes=classes, subjects=subjects)
    gra = int(request.form.get("grade"))
    sub = int(request.form.get("subject"))
    # Fetch data from the database
    result = db.execute(query, id, gra, sub)

    result_list = []
    for row in result:
        name = row['Name']
        marks = row['Marks']
        average = row['Average']
        test_id = row['TestID']
        test_name = row['TestName']
        # Append data to the result_list
        result_list.append({'Name': name, 'Marks': marks, 'Average': average, 'TestID': test_id, 'TestName': test_name})

    # Return JSON response for AJAX requests
    if request.is_json:
        return jsonify(result_list)

    return render_template("analyse.html",  classes=classes, subjects=subjects, data=json.dumps(result))

# Creating an accont for new user
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Retriving form values
        name = request.form.get("username")
        passwd = request.form.get("password")
        repasswd = request.form.get("confirmation")
        users = db.execute("SELECT username FROM users")
        # Validating
        if not name:
            return apology("Must provide name")
        elif name in [user["username"] for user in users]:
            return apology("Username already taken")
        elif not passwd:
            return apology("Must set a password")
        elif not repasswd:
            return apology("Must confirm password")
        elif passwd != repasswd:
            return apology("Passwords don't match")
        else:
            # Registering user if validation successful
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                name,
                generate_password_hash(passwd),
            )
            id = db.execute("SELECT * FROM users WHERE username = ?", name)
            # Logging the user in
            session["user_id"] = id[0]["id"]
            flash("You have been registered and logged in successfully.")
            return redirect("/")
    # IF GET method is used
    return render_template("signup.html")

#Log user in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    # User reached route via POST
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        flash("Welcome Back !!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#Log user out
@app.route("/logout")
@login_required
def logout():
    #Forget any user_id
    session.clear()
    #Redirect user to login form
    return redirect("/login")
