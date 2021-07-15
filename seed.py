from app import app
from models import db, User, Post

# Create all tables
db.drop_all()
db.create_all()

#create users in the users table
zach = User(first_name="Zach", last_name="Thomas")
ivan = User(first_name="Ivan", last_name="Yang")
nate = User(first_name="Nate", last_name="Lipp", img_url="https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/nate/370ea80d-671c-4b93-96e2-c1b6f426b705-nate-image/00f4acdacbc49080a9db86c7c3d9c616.jpg")





db.session.add_all([zach, ivan, nate])

db.session.commit()

# Create test posts for test users
testpost1 = Post(title='Test post 1', content='Content for test post 1', user_id=zach.id)

testpost2 = Post(title='Test post 2testpost2', content='Content for test post 2testpost2', user_id=zach.id)

testpost3 = Post(title='Test post 3', content='Content for test post 3', user_id=zach.id)

testpost4 = Post(title='Test post 4', content='Content for test post 4', user_id=ivan.id)

testpost5 = Post(title='Test post 5', content='Content for test post 5', user_id=ivan.id)

db.session.add_all([testpost1, testpost2, testpost3, testpost4, testpost5])

db.session.commit()