import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    assets = 0
    data = db.execute("SELECT * FROM stonks WHERE id = ?", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    for stonk in data:
        assets += stonk["shares"] * lookup(stonk["symbol"])["price"]
    return render_template(
        "index.html", data=data, cash=cash[0]["cash"], lookup=lookup, assets=assets
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        id = session["user_id"]
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("Which stock ?")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Shares should be positive integer")
        user = db.execute("SELECT * FROM users WHERE id = ?", id)
        cost = symbol["price"] * shares
        if shares < 1:
            return apology("Can't short stocks")
        elif cost > user[0]["cash"]:
            return apology("Insufficient funds")
        else:
            select = db.execute(
                "SELECT * FROM stonks WHERE id = ? AND symbol = ?", id, symbol["symbol"]
            )
            update = "UPDATE stonks SET shares = ? WHERE id = ? AND symbol = ?"
            insert = "INSERT INTO stonks (id, symbol, name, shares) VALUES (?,?,?,?)"
            history = (
                "INSERT INTO history (hid, symbol, change, price) VALUES (?,?,?,?)"
            )
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", user[0]["cash"] - cost, id
            )
            if select:
                db.execute(update, shares + select[0]["shares"], id, symbol["symbol"])
                db.execute(history, id, symbol["symbol"], shares, symbol["price"])
            else:
                db.execute(insert, id, symbol["symbol"], symbol["name"], shares)
                db.execute(history, id, symbol["symbol"], shares, symbol["price"])
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    data = db.execute(
        "SELECT history.* FROM history JOIN stonks ON history.hid = stonks.hid WHERE stonks.id = ?",
        session["user_id"],
    )
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        if None == info:
            return apology("STOCK doesn't exist")
        else:
            dollars = usd(info["price"])
            return render_template("quoted.html", name=info["name"], price=dollars)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        passwd = request.form.get("password")
        repasswd = request.form.get("confirmation")
        users = db.execute("SELECT username FROM users")
        if not name:
            return apology("Must provide name")
        elif not passwd:
            return apology("Must set a password")
        elif not repasswd:
            return apology("Must confirm password")
        elif passwd != repasswd:
            return apology("Passwords doesn't match")
        elif name in [user["username"] for user in users]:
            return apology("Username already taken")
        else:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                name,
                generate_password_hash(passwd),
            )
            id = db.execute("SELECT * FROM users WHERE username = ?", name)
            session["user_id"] = id[0]["id"]
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    id = session["user_id"]
    data = db.execute("SELECT * FROM stonks where id = ? AND shares > 0", id)
    if request.method == "POST":
        history = "INSERT INTO history (hid, symbol, change, price) VALUES (?,?,?,?)"
        symbol = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        stonk = db.execute(
            "SELECT * FROM stonks where id = ? AND symbol = ?", id, symbol["symbol"]
        )
        cash = db.execute("SELECT * FROM users WHERE id = ?", id)[0]["cash"]
        net = shares * symbol["price"]
        if shares > stonk[0]["shares"]:
            return apology("Not enough shares owned")
        else:
            upstock = "UPDATE stonks SET shares = ? WHERE id = ? AND symbol = ?"
            upcash = "UPDATE users SET cash = ? WHERE id = ?"
            db.execute(upstock, stonk[0]["shares"] - shares, id, symbol["symbol"])
            db.execute(upcash, cash + net, id)
            db.execute(
                history, id, symbol["symbol"], "-" + str(shares), symbol["price"]
            )
            return redirect("/")
    else:
        return render_template("sell.html", data=data)

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user = db.execute("SELECT * FROM users where id = ?", session["user_id"])
    if request.method == "POST":
        id = session["user_id"]
        opasswd = request.form.get("opasswd")
        npasswd = request.form.get("npasswd")
        confirm = request.form.get("cpasswd")
        if not opasswd:
            return apology("Must provide old password")
        elif not npasswd:
            return apology("Must set a new password")
        elif not confirm:
            return apology("Must confirm password")
        elif not check_password_hash(user[0]["hash"], opasswd):
            return apology("Incorrect password")
        elif npasswd != confirm:
            return apology("Passwords doesn't match")
        else:
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?",
                  generate_password_hash(npasswd),
                    id)
            return render_template("changed.html", user=user[0]["username"])
    else :
        return render_template("account.html", user=user[0]["username"])
