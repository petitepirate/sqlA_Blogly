"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
