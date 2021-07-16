"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post

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
    """display the user's details"""
    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)
    

@app.route('/users/<user_id>/edit')
def display_edit_user_form(user_id):
    """display form to edit user's details"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_existing_user(user_id):
    """edit user details in the database"""
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
    """Deletes the user from the database"""
    user = User.query.get_or_404(user_id)
    posts = user.posts
    
    for post in posts:
        db.session.delete(post)
        
    db.session.commit()
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>/posts/new')
def display_new_post_form(user_id):
    """render the HTML to make a new post for the user"""
    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)

@app.route('/users/<user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """Creates a new post and adds it to the database then redirects to user's page"""
    user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    
    user.posts.append(post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')
    
@app.route('/posts/<post_id>')
def display_post_detail(post_id):
    """render the post details"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<post_id>/edit')
def display_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<post_id>/edit', methods=['POST'])
def make_post_edits(post_id):
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()


    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/users')
