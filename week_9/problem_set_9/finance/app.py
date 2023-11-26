import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

import datetime

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
    positions = get_user_positions(session["user_id"])
    cash = get_user_cash(session["user_id"])

    sum = cash
    for position in positions:
        sum += position["total"]

    return render_template("index.html", positions=positions, cash=cash, sum=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock_data = lookup(symbol.upper())

        if stock_data == None:
            return apology("incorrect symbol")

        try:
            shares = float(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a number")

        if shares <= 0 or not shares.is_integer():
            return apology("shares must be a positive whole number")

        transaction_value = shares * stock_data["price"]

        user_id = session["user_id"]

        user_cash = get_user_cash(user_id)

        if user_cash < transaction_value:
            return apology("not enough liquidity")

        new_balance = user_cash - transaction_value

        # update user cash balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   new_balance, user_id)

        unix_timestamp = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock_data["symbol"], shares, stock_data["price"], unix_timestamp)

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol")

        stock_data = lookup(symbol.upper())

        if stock_data == None or not stock_data:
            return apology("incorrect symbol")

        return render_template("quoted.html", symbol=stock_data["symbol"], name=stock_data["name"], price=stock_data["price"])

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) > 0:
            return apology("user already exists", 400)

        password_hash = generate_password_hash(request.form.get("password"))

        user = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), password_hash)

        # Remember which user has logged in
        session["user_id"] = user

        # Redirect user to home page
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("invalid symbol")

        if shares <= 0:
            return apology("must provide shares greater than 0")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]

        user_cash = get_user_cash(user_id)

        user_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)[0]["shares"]

        if shares > user_shares:
            return apology("not enough shares")

        uptd_cash = user_cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   uptd_cash, user_id)

        unix_timestamp = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1)*shares, stock["price"], unix_timestamp)

        return redirect("/")

    positions = get_user_positions(session["user_id"])
    return render_template("sell.html", positions=positions)


def get_user_positions(user_id):
    return db.execute("SELECT symbol, SUM(shares) as shares, price, SUM(shares * price) as total FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)


def get_user_cash(user_id):
    user_res = db.execute(
        "SELECT cash FROM users WHERE id = ?", user_id)

    return user_res[0]["cash"]
