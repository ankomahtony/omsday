from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.Date ,nullable=True)
    church = db.Column(db.String(100),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Pastor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    wife = db.Column(db.String(100),nullable=False)
    wife_image = db.Column(db.String(20),nullable=False, default='default_wife.jpg')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    bio = db.Column(db.Text, nullable=False)    

    def __repr__(self):
        return f"Pastor('{self.name}',{self.wife}"


class Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    loc = db.Column(db.String(100),nullable=False)
    est = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    members = db.Column(db.Integer,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_church.jpg')

    def __repr__(self):
        return f"Sermon('{self.name}','{self.loc}'"
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False, default='Beliefs')
    subtitle = db.Column(db.String(240), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Sermon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False, default='Beliefs')
    subtitle = db.Column(db.String(240), nullable=False)
    message = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_sermon.jpg')
    video_file = db.Column(db.String(20), nullable=False, default='default.mp4')
    comments = db.relationship('Comment', backref='sermon', lazy=True)

    def __repr__(self):
        return f"Sermon('{self.title}',{self.date_posted})"

class UpEvent(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    event = db.Column(db.String(100),nullable=False)
    start_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date, nullable=False)
    loc = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_event.jpg')
    facilatator = db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return f"UpEvent('{self.event}','{self.facilatator}')"
        
class Donation(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    target = db.Column(db.Integer,nullable=False)
    received = db.Column(db.Integer,nullable=False)
    message = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='default_donation.jpg')
    
    def __repr__(self):
        return f"Donation('{self.title}','{self.target}')"

class Past_P(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    program = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Past_P('{self.program}','{self.image_file}')"
        
class Quote(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(200),nullable=False)
    message = db.Column(db.Text)
    ref = db.Column(db.String(100))

    def __repr__(self):
        return f"Quote('{self.message}','{self.author}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    sermon_id = db.Column(db.Integer, db.ForeignKey('sermon.id'), nullable=True)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.date_posted}')"

