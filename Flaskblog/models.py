from datetime import datetime
from Flaskblog import db,login_manager
from flask_login import UserMixin

#class that will add many attributes-UserMixin provides
#  default attributes and methods

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # gets user with that id
 
class User(db.Model,UserMixin):
    '''
     User parent class inherits from db.Model,UserMixin -   
     This provides default implementations for the methods that Flask-Login
     expects user objects to have.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # backref-adding another column if we have apost we can get ts author

#    this method specifies how the object will be printed out
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    """

        Post class

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    content= db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title }','{self. date_posted}')"
