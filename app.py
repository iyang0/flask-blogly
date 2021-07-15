"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "gfudhiaskhjl543278489grhuiger8934"
debug = DebugToolbarExtension(app)

@app.route("/")
def root():
    """redirects to the list of users"""
    return redirect('/users')
    

@app.route("/users")
def users_view():
    """gets and displays the users from database"""
    users = User.query.all()
    return render_template('user_list.html',
        users=users) 


@app.route('/users/new')
def create_new_user():
    """render form to create a new user"""
    return render_template('new_user.html')

@app.route('/user_detail')
def display_user_details():
    user = User.query.first()

    return render_template('user_detail.html', user=user)
    

@app.route('/edit_user')
def edit_existing_user():

    return render_template('edit_user.html')
    