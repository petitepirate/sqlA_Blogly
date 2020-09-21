"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.debug = False
app.config['SECRET_KEY'] = "asdfjkl"
debug = DebugToolbarExtension(app)


@app.route("/")
# to be fixed later
def home():
    return redirect("/users")


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route("/users")
def list_users():
    """List users and show add form button"""

    users = User.query.all()

    return render_template("index.html", users=users)


@app.route("/users/new")
def users_new_form():
    """Show a form to create a new user"""
    users = User.query.all()
    return render_template('usersform.html', users=users)


@app.route("/users/new", methods=["POST"])
def user_entry():
    """Create a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show details of a pet"""
    user = User.query.get_or_404(user_id)
    image_url = user.image_url
    print(image_url)
    return render_template("userdeets.html", user=user, image_url=image_url)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit form"""
    user = User.query.get_or_404(user_id)
    return render_template("editform.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    """Edit a user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
###################################################################
# Exercise 2 start


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Show edit form"""
    user = User.query.get_or_404(user_id)
    return render_template("newpostform.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """new post"""
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'], user=user
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_page(post_id):
    """Page for each post"""

    post = Post.query.get_or_404(post_id)
    return render_template('postspage.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edit a post"""

    post = Post.query.get_or_404(post_id)
    return render_template('editpostform.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
