from flask import Blueprint, render_template, request, flash, redirect, url_for

from functools import wraps

from website.models.user import User

account = Blueprint('account',
                    __name__,
                    template_folder="../templates/account",
                    url_prefix='/account')


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*arg, **kwargs):
        userid = request.cookies.get('userid')
        if userid:
            user = User.get_user_by_user_id(userid)
            if user:
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
    if not user:
        return 'login failed!'
    response = redirect(url_for("account.login_success"))
    response.set_cookie('userid', user.userid)
    return response


@account.route("/login_success/")
@login_required
def login_success():
    user = User.get_user_by_user_id(request.cookies['userid'])
    return render_template("login_success.html", user=user)


@account.route("/register/", methods=['GET', 'POST'])
def register():
    return render_template('registration_form.html')

@account.route("/logout/", methods=['GET'])
def logout():
    return 'logout'
