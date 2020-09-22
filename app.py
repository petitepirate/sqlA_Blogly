"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag

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
def home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Page"""

    return render_template('404.html'), 404


@app.route("/users")
def list_users():
    """List users and show add form button"""

    users = User.query.order_by(User.last_name, User.first_name).all()

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
    flash(f"User {new_user.first_name} {new_user.last_name} added.")

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """show details of a pet"""
    user = User.query.get_or_404(user_id)
    image_url = user.image_url

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
    flash(f"User edited.")

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User deleted.")

    return redirect("/users")
###################################################################
# Exercise 2 start


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Show edit form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()  # Exercise 3 Addition

    # Exercise 3 Addition
    return render_template("newpostform.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """new post"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist(
        "tags")]  # Exercise 3 Addition
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()  # Exercise 3 Addition

    new_post = Post(
        title=request.form['title'],
        # Exercise 3 Addition
        content=request.form['content'], user=user, tags=tags
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post added")

    return redirect(f"/users/{user_id}")


@app.route("/posts")
def all_posts():
    posts = Post.query.order_by(Post.created_at.desc()).limit(30).all()

    return render_template('allposts.html', posts=posts)


@app.route('/posts/<int:post_id>')
def posts_page(post_id):
    """Page for each post"""

    post = Post.query.get_or_404(post_id)
    return render_template('postspage.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Edit a post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()  # Exercise 3 Addition
    # Exercise 3 Addition
    return render_template('editpostform.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(
        tag_ids)).all()  # Exercise 3 Addition

    db.session.add(post)
    db.session.commit()
    flash(f"Post updated")

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post deleted")

    return redirect(f"/users/{post.user_id}")

###################################################################
# Exercise 3 start


@app.route('/tags')
def list_tags():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/new')
def new_tag_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('newtagform.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def submit_tag():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag added")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tagdetails.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edittagform.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_tag_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag deleted.")

    return redirect("/tags")
