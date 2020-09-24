from unittest import TestCase

from app import app
from models import db, User, Post, PostTag, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        # User.query.delete()

        crosby = User(first_name="Sidney", last_name="Crosby",
                      image_url="https://images.unsplash.com/photo-1517177646641-83fe10f14633?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80")
        db.session.add(crosby)
        db.session.commit()

        self.user_id = crosby.id
        self.user = crosby

        """Add sample post."""
        # Post.query.delete()
        crosbypost = Post(title="Its Hockey Season!",
                          content="Are you ready to watch some hockey!?", user_id=crosby.id)
        db.session.add(crosbypost)
        db.session.commit()

        self.post_id = crosbypost.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """tests /users route"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)

    def test_show_user(self):
        """test user-details route"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Sidney Crosby Details</h1>', html)

    def test_create_user(self):
        """tests create-users route"""
        with app.test_client() as client:
            resp = client.get(f"/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Add User:</h2>', html)

    def test_add_user(self):
        with app.test_client() as client:
            user2 = {
                "first_name": "Test", "last_name": "Testing",
                "image_url": ""
            }
            resp = client.post("/users/new", data=user2,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)  
            # self.assertIn('Test User2', html)

    # def test_edit_user_route(self):
    #     """tests edit-user route"""
    #     with app.test_client() as client:
    #         resp = client.get(f"/users/{self.user_id}/edit")
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn('<h2>Edit User:</h2>', html)

    # def test_edit_user(self):
    #     with app.test_client() as client:
    #         user = {
    #             'first-name': 'Test',
    #             'last-name': 'User-Edit'
    #         }
    #         resp = client.post(
    #             f'users/{self.user_id}/edit', data=user, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
           # self.assertIn('Test User-Edit', html)

    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         client.get(f'/users/{self.user_id}')
    #         resp = client.post(
    #             f'/users/{self.user_id}/delete', follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)
            # self.assertNotIn('Sidney Crosby', html)

    # BLOG POST TESTS
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Its Hockey Season!', html)
            self.assertIn('Are you ready to watch some hockey!?', html)

    def test_add_post(self):
        with app.test_client() as client:
            post = {
                'title': 'Ovechkin Sucks',
                'content': 'Yup, I said it!',
                'user_id': self.user_id
            }
            resp = client.post(
                f'/users/{self.user_id}/posts/new', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
    #         self.assertIn('Ovechkin Sucks', html)
    #         self.assertIn('Yup, I said it!', html)

    def test_edit_post(self):
        with app.test_client() as client:
            post = {
                'title': 'Test Edit Post',
                'content': 'Test edited content'
            }
            resp = client.post(
                f'/posts/{self.post_id}/edit', data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # self.assertIn('Test Edit Post', html)
            # self.assertIn('Test edited content', html)
