"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "gfudhiaskhjl543278489grhuiger8934"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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
def display_new_user_form():
    """render form to create a new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    """render form to create a new user"""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url'] or None

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    # todo: redirect to /users
    return redirect('/')

@app.route('/users/<user_id>')
def display_user_details(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)
    

@app.route('/users/<user_id>/edit')
def display_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_existing_user(user_id):
    user = User.query.get_or_404(user_id)
    if(request.form['first-name'] != ''):
        user.first_name = request.form['first-name']
    if(request.form['last-name'] != ''):
        user.last_name = request.form['last-name']
    user.img_url = request.form['img-url'] or None

    db.session.add(user)
    db.session.commit()


    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # User.query.filter(User.id==user_id).delete()
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>/posts/new')
def display_new_post_form(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)