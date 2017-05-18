from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import hashlib

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    @classmethod
    def validate_email(self, email):
        return User.query.filter_by(email=email).first()
    @classmethod
    def validate_username(self, username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod                             #添加虚拟用户
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(),
                     password=forgery_py.lorem_ipsum.word(),
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def gravator(self, size=100, default='identicon', rating='g'):
        url = 'http://www.gravatar.com/avatar'
        if self.avatar_hash:
            hash = self.avatar_hash
        else:
            hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
            self.avatar_hash = hash
            db.session.add(self)
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                        url=url, hash=hash, size=size, default=default, rating=rating)

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    tag = db.Column(db.String(64))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            # u = User.query.offset(randint(0,user_count-1)).first()
            u = User.query.filter_by(admin=True).first()
            p = Post(title=forgery_py.name.full_name(),
                     tag=forgery_py.name.full_name(),
                     content=forgery_py.lorem_ipsum.sentences(randint(3, 30)),
                     author=u)
            db.session.add(p)
            db.session.commit()

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(50), nullable=False)
    user_image = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '<Comment {}>'.format(self.content)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))