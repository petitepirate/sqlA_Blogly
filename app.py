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
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
# to be fixed later
def home():
    return redirect("/users")


@app.route("/users")
# Show all users.
def list_users():
    """List users and show add form button"""
# Make these links to view the detail page for the user.
    users = User.query.all()

    return render_template("index.html", users=users)
# Have a link here to the add-user form.


@app.route("/users/new", method=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('usersform.html')


# @app.route("/users/new", methods=["POST"])
# def user_entry():
#     """Handle form submission for creating a new user"""

#     # new_user = User(
#     #     first_name=request.form['first_name'],
#     #     last_name=request.form['last_name'],
#     #     image_url=request.form['image_url'])

#     # db.session.add(new_user)
#     # db.session.commit()

#     return redirect("/users")
# GET / users/[user-id]
# # Show information about the given user.

# # Have a button to get to their edit page, and to delete the user.

# GET / users/[user-id]/edit
# # Show the edit page for a user.

# # Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# POST / users/[user-id]/edit
# # Process the edit form, returning the user to the /users page.
# POST / users/[user-id]/delete
# # Delete the user.
