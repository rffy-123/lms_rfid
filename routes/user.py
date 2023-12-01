from flask import Blueprint, g, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from flask import jsonify
from Misc.functions import *

from Controllers.UserManager import UserManager

user_view = Blueprint('user_routes', __name__, template_folder='/templates')

user_manager = UserManager(DAO)

@user_view.route('/', methods=['GET'])
def home():
	g.bg = 1

	user_manager.user.set_session(session, g)
	print(g.user)

	return render_template('home.html', g=g)


@user_view.route('/signin', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signin():
    if request.method == 'POST':
        _form = request.form
        password = str(_form["password"])
        # Assuming 'rfid' is the name of the RFID field in the form
        rfid = request.form.get('rfid')

        if len(password) < 1:
            return render_template('signin.html', error="Password is required")

        # Additional logic to handle RFID
        if rfid:
            # Use the RFID data to fetch user information from the database
            user_info = user_manager.get_user_by_rfid(rfid)

            if user_info and user_manager.verify_password(password, user_info['password']):
                # Pre-fill the session with user information
                session['user'] = int(user_info['id'])
                return redirect("/")

            # Handle the case when RFID doesn't match any user or password is incorrect
            return render_template('signin.html', error="RFID not recognized or password incorrect")

        # Handle the case when RFID is not provided
        return render_template('signin.html', error="RFID is required")

    return render_template('signin.html')


@user_view.route('/signup', methods=['GET', 'POST'])
@user_manager.user.redirect_if_login
def signup():
    if request.method == 'POST':
        rfid = request.form.get('rfid')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(name) < 1 or len(email) < 1 or len(password) < 1:
            return render_template('signup.html', error="All fields are required")

        new_user = user_manager.signup(name, email, hash(password), rfid)

        if new_user == "already_exists":
            return render_template('signup.html', error="User already exists with this email")

        return render_template('signup.html', msg="You've been registered!")

    return render_template('signup.html')


@user_view.route('/signout/', methods=['GET'])
@user_manager.user.login_required
def signout():
	user_manager.signout()

	return redirect("/", code=302)

@user_view.route('/user/', methods=['GET'])
@user_manager.user.login_required
def show_user(id=None):
	user_manager.user.set_session(session, g)
	
	if id is None:
		id = int(user_manager.user.uid())

	d = user_manager.get(id)
	mybooks = user_manager.getBooksList(id)

	return render_template("profile.html", user=d, books=mybooks, g=g)

@user_view.route('/user', methods=['POST'])
@user_manager.user.login_required
def update():
    user_manager.user.set_session(session, g)

    _form = request.form
    rfid = _form.get('rfid')
    name = str(_form["name"])
    email = str(_form["email"])
    password = str(_form["password"])
    bio = str(_form["bio"])


    user_manager.update(name, email, hash(password), bio, user_manager.user.uid(), rfid)

    flash('Your info has been updated!')
    return redirect("/user/")