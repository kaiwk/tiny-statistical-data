from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, session)

from functools import wraps

from website.models.user import User

account = Blueprint('account',
                    __name__,
                    template_folder="../templates/account",
                    url_prefix='/account')

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*arg, **kwargs):
        userid = session.get('userid')
        if userid is not None:
            user = User.get_user_by_user_id(userid)
            if user is not None:
                return view_func(*arg, **kwargs)
            else:
                flash('Session exsits, but user does not exsit')
                return redirect(url_for('account.login'))
        else:
            flash('Please login')
            return redirect(url_for('account.login'))
    return wrapper


@account.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    # post
    username = request.form['username']
    password = request.form['password']
    user = User.validate_and_login(username, password)
    if user is None:
        flash("username or password is not match.")
        return redirect(url_for('account.login'))
    session['userid'] = user.userid
    return redirect(url_for('statistics.index'))

@account.route("/logout/", methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('statistics.index'))

@account.route("/login_success/")
@login_required
def login_success():
    user = User.get_user_by_user_id(session['userid'])
    return render_template("login_success.html", user=user)


@account.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration_form.html')
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']
    if password != confirm:
        flash('password is not same as confirmed.')
        return redirect(url_for("account.register"))
    if not User.validate_and_register(username, email, password):
        flash('username conflict! please change another username.')
        return redirect(url_for('account.register'))
    flash("Register Success.")
    return redirect(url_for('account.login'))
