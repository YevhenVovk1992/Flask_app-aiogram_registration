import os
from typing import Union

import dotenv
from flask import Flask, request, render_template, redirect, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug import Response
from werkzeug.security import check_password_hash

import database
import models
from form import LoginForm


# Loading environment variables into the project
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SESSION_SECRET')
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    since the user_id is just the primary key of our user table, use it in the query for the user
    """
    return models.User.query.get(int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    """
    This function closes the connection to the database after the view function is executed
    """
    database.db_session.remove()


@app.route('/', methods=('GET',))
def index() -> Union[str, Response]:
    """
    The function renders start page.
    """
    return render_template('index.html')


@app.route('/signup', methods=('GET', 'POST'))
def signup() -> Union[str, Response]:
    """
    The function is redirecting the user to telegram bot
    """

    bot_id = os.environ.get('BOT_ID')
    return redirect(f'https://telegram.me/{bot_id}')


@app.route('/profile', methods=('GET', ))
@login_required
def profile() -> Union[str, Response]:
    """
    The function renders the page with user info
    """
    data = {
        'login': current_user.login,
        'first_name': current_user.first_name,
        'age': current_user.age,
        'gender': current_user.gender,
        'telegram_id': current_user.telegram_id,
        'telegram_username': '@' + current_user.telegram_username
    }
    return render_template('profile.html', data=data)


@app.route('/login', methods=('GET', 'POST'))
def login() -> Union[str, Response]:
    """
    The function renders a page with a login form
    """
    if request.method == "GET":
        form = LoginForm()
        return render_template('login.html', form=form)
    else:
        name = request.form.get('login')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = models.User.query.filter_by(login=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect('/login')
        login_user(user, remember=remember)
        return redirect('/profile')


@app.route('/logout', methods=('GET',))
@login_required
def logout() -> Union[str, Response]:
    """
    The function logout the user and redirect to index page
    :return: HTML
    """
    logout_user()
    flash('You have successfully logged yourself out')
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG'))
