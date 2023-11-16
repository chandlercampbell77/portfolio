from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup
import html
import random

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///trivia.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show homepage"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":

        users = db.execute("SELECT * FROM users;")

        # if no users, then a new user must be created
        if not users:
            return render_template("register.html")

        # otherwise, users exist, so we can give the user the homepage
        user = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        username = user[0]["username"]
        return render_template("index.html", user=username)

    # handling case where they clicked the play button
    else:
        return render_template("play.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))

        # Ensure username exists
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        # ensure password matches confirmation
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # complete registration of user
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get("username"), hash)
        user = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))
        session["user_id"] = user[0]["id"]

        # present user the homepage
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    """Show user question options"""
    if request.method == "GET":
        return render_template("play.html")
    else:
        # grab input from user
        amount = 5
        category = request.form.get("category")
        difficulty = request.form.get("difficulty")
        type = request.form.get("type")

        # ensure user submitted all fields
        if not category:
            return apology("must provide category", 400)
        if not difficulty:
            return apology("must provide difficulty", 400)
        if not type:
            return apology("must provide type", 400)

        # retrieve questions based on user input
        global trivia
        trivia = lookup(amount, category, difficulty, type)

        # handle case where retrieval fails
        if len(trivia) != amount:
            return apology("trivia questions of that category, difficulty, and type not found", 400)

        # collect answers in list to display to user
        answers = []
        for i in range(amount):
            answers.append(i)
        for i in range(amount):
            answers[i] = trivia[i]["incorrect_answers"]
            answers[i].insert(random.randint(0, len(answers[i])), trivia[i]["correct_answer"])

        return render_template("quiz.html", trivia=trivia, amount=amount, html=html, answers=answers, len=len)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    """Show trivia questions"""
    if request.method == "GET":
        return render_template("play.html")
    else:
        # retrieve the answers the user picked and put them in a list
        answer = []
        answer.append(request.form.get("question0"))
        answer.append(request.form.get("question1"))
        answer.append(request.form.get("question2"))
        answer.append(request.form.get("question3"))
        answer.append(request.form.get("question4"))

        # amount of questions is constant
        amount = 5

        # evaluate answers for correctness and update database accordingly
        feedback = []
        for i in range(amount):
            if answer[i] != None:
                db.execute("UPDATE users SET answered = answered + 1 WHERE id = ?;", session["user_id"])
                db.execute("INSERT INTO history (question, user_answer, correct_answer, user_id) VALUES (?, ?, ?, ?);", html.unescape(trivia[i]["question"]), answer[i], html.unescape(trivia[i]["correct_answer"]), session["user_id"])
            if answer[i] == html.unescape(trivia[i]["correct_answer"]):
                db.execute("UPDATE users SET points = points + 100 WHERE id = ?;", session["user_id"])
                db.execute("UPDATE users SET correct = correct + 1 WHERE id = ?;", session["user_id"])
                feedback.append("Correct! +100 points")
            else:
                feedback.append("Incorrect! No points added.")
                if answer[i] != None:
                    db.execute("UPDATE users SET incorrect = incorrect + 1 WHERE id = ?;", session["user_id"])

        return render_template("results.html", trivia=trivia, amount=amount, html=html, answer=answer, feedback=feedback)


@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    """Show results"""
    # if user mistakenly types in /results into the address bar, redirect them to the homepage
    if request.method == "GET":
        return redirect("/")

    # if the user clicks the play again button
    else:
        return render_template("play.html")


@app.route("/history")
@login_required
def history():
    """Display all questions answered previously"""
    if request.method == "GET":
        history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY time DESC;", session["user_id"])
        return render_template("history.html", history=history)


@app.route("/leaderboard")
@login_required
def leaderboard():
    """Display the rankings of the users"""
    if request.method == "GET":
        leaderboard = db.execute("SELECT * FROM users ORDER BY points DESC;")
        return render_template("leaderboard.html", leaderboard=leaderboard, format=format)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Allow user to change their password"""
    if request.method == "GET":
        return render_template("password.html")
    else:
        # Ensure each password was submitted
        if not request.form.get("currentpassword") or not request.form.get("newpassword") or not request.form.get("confirmpassword"):
            return apology("must fill in all fields", 400)

        # ensure user entered correct password
        user = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        if not check_password_hash(user[0]["hash"], request.form.get("currentpassword")):
            return apology("current password entered does not match database", 400)

        # ensure new password matches password confirmation
        if request.form.get("newpassword") != request.form.get("confirmpassword"):
            return apology("new password does not match confirmation", 400)

        # update database to reflect user's new password
        newhash = generate_password_hash(request.form.get("newpassword"))
        db.execute("UPDATE users SET hash = (?) WHERE id = (?);", newhash, session["user_id"])

        # tell user it worked
        flash("Password changed successfully!")

        return redirect("/")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Allow user to delete their account"""
    if request.method == "GET":
        user = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        username = user[0]["username"]
        return render_template("delete.html", user=username)
    else:
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])

        # Ensure password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid password", 400)

        # delete user from database
        db.execute("DELETE FROM users WHERE id = ?;", session["user_id"])
        db.execute("DELETE FROM history WHERE user_id = ?;", session["user_id"])

        # log user out
        session.clear()

        # tell user it worked
        flash("Account successfully deleted.")

        # prompt them to register again
        return render_template("register.html")