from unittest import TestCase
from app import app
from models import db, User

# Make Flask errors be real errors, not HTML pages with error info

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True


db.drop_all()
db.create_all()

class BloglyAppTestCase(TestCase):
    
    def setUp(self):
        """Stuff to do before every test."""
        User.query.delete()
        self.client = app.test_client()
        
        zach = User(first_name="Test user", last_name="1", img_url='')
        ivan = User(first_name="Test user", last_name="2", img_url='')
        db.session.add_all([zach, ivan])
        db.session.commit()
        self.user1 = zach
        self.user2 = ivan
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
    def test_root(self):
        """Make sure that the root redirects correctly """
        with self.client as client:
            response = client.get('/')
            
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "http://localhost/users")
            
    def test_access_new_user_form(self):
        """Tests that we can make GET request to new user form"""
        with self.client as client:
            
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            
            self.assertIn('id="create-user"', html)
            
    def test_creating_new_user_from_form(self):
        """Send a post request hitting the /users/new form"""
        with self.client as client:
            
            response = client.post('/users/new',
                data = {
                    "first-name": "API",
                    "last-name": "Test",
                    "img-url": "https://media.wired.com/photos/5bb532b7f8a2e62d0bd5c4e3/1:1/w_1800,h_1800,c_limit/bee-146810332.jpg"
                })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "http://localhost/")
            self.assertEqual(User.query.
                filter(User.first_name=="API").
                one().
                first_name,
                "API")
            
    def test_creating_edit_user_from_form(self):
        """Send a post request hitting the /users/<user_id>/edit form"""
        
        with self.client as client:
            # test_user = User.query.filter(User.first_name=="Ivan").first()
            d= {
                "first-name": "API2",
                "last-name": "Test2",
                "img-url": "https://media.wired.com/photos/5bb532b7f8a2e62d0bd5c4e3/1:1/w_1800,h_1800,c_limit/bee-146810332.jpg"
                }
            response = client.post(f'/users/{self.user2.id}/edit',
                data = d,
                follow_redirects=True)
                    
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(f"{d['first-name']} {d['last-name']}", html)
