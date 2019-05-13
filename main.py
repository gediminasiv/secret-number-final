import random
import uuid
import hashlib
from flask import Flask, render_template, request, make_response
from flask import redirect
from flask import url_for

from models import User

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get('session_token')

    user = User.fetch_one(query=["session_token", "==", session_token])

    response = make_response(render_template("index.html", user=user))

    return response

@app.route("/login", methods=["POST"])
def login():
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    user = User.fetch_one(query=["email", "==", user_email])

    if not user:
        new_secret = random.randint(1, 30)

        user = User(email=user_email, password=hashed_password, secret_number=new_secret, session_token='')

        user.create()

    if hashed_password != user.password:
        return 'Your password was entered badly'
    elif hashed_password == user.password:
        session_token = str(uuid.uuid4())

        User.edit(obj_id=user.id, session_token=session_token)

        response = make_response(redirect(url_for('index')))

        response.set_cookie('session_token', session_token, httponly=True, samesite='Strict')

        return response

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('index')))

    response.set_cookie('session_token', expires=0)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    session_token = request.cookies.get('session_token')

    user = User.fetch_one(query=["session_token", "==", session_token])

    secret_number = user.secret_number

    if guess == secret_number:
        message = "Correct! The secret number is {0}".format(str(secret_number))
        response = make_response(render_template("result.html", message=message, user=user))

        new_secret = random.randint(1, 30)

        User.edit(obj_id=user.id, secret_number=new_secret)

        return response
    elif guess > secret_number:
        message = "Your guess is not correct... try something smaller."
        return render_template("result.html", message=message, user=user)
    elif guess < secret_number:
        message = "Your guess is not correct... try something bigger."
        return render_template("result.html", message=message, user=user)


if __name__ == '__main__':
    app.run(debug=True)
