import os
import dotenv

from flask import Flask, request, render_template, redirect, abort
from typing import Union
from werkzeug import Response


import database
from form import LoginForm


# Loading environment variables into the project
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SESSION_SECRET')


# This function closes the connection to the database after the view function is executed
@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    database.db_session.remove()


@app.route('/', methods=('GET', ))
def index() -> Union[str, Response]:
    """
    The function renders start page.
    :return: HTML
    """
    return render_template('index.html')


@app.route('/profile', methods=('GET', ))
def profile() -> Union[str, Response]:
    """
    The function renders the page with user info.
    :return: HTML
    """
    return render_template('profile.html', title='Profile')


@app.route('/login', methods=('GET', 'POST'))
def login() -> Union[str, Response]:
    """
    The function renders a page with a login form.
    :return: HTML
    """
    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route('/logout', methods=('GET', ))
def logout() -> Union[str, Response]:
    """
    The function renders the page with user info.
    :return: HTML
    """
    return 'logout'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG'))
