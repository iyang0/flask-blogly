from app import app
from models import db, User

# Create all tables
db.drop_all()
db.create_all()

#create users in the users table
zach = User(first_name="Zach", last_name="Thomas")
ivan = User(first_name="Ivan", last_name="Yang")
nate = User(first_name="Nate", last_name="Lipp", img_url="https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/nate/370ea80d-671c-4b93-96e2-c1b6f426b705-nate-image/00f4acdacbc49080a9db86c7c3d9c616.jpg")

db.session.add_all([zach, ivan, nate])

db.session.commit()