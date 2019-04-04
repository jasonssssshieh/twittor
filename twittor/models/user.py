from twittor import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #提供用户session管理的基本方法
from hashlib import md5
from flask import current_app
import jwt, time
from twittor.models.tweet import Tweet

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

"""
这个table的含义就是:
follower_id | followed_id 里面有follower 然后关注了followed这个人
"""


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default = datetime.utcnow)
    is_activated = db.Column(db.Boolean, default = False)

    tweets = db.relationship('Tweet', backref = 'author', lazy = 'dynamic') 
    """ 这里Tweet是大写"""

    followed  = db.relationship(
        'User', secondary = followers,
        primaryjoin = (followers.c.follower_id == id),#我关注了多少人
        secondaryjoin = (followers.c.followed_id == id),#我被多少人关注
        backref = db.backref('followers', lazy = 'dynamic'), lazy = 'dynamic'
    )

    def __repr__(self):
        return 'id = {}, username = {}, email = {}, password_hash = {}'.format(
            self.id, self.username, self.email, self.password_hash
        )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size = 80):
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            md5_digest, size
        )
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def own_and_followed_tweets(self):
        own = Tweet.query.filter_by(user_id = self.id)#我自己的tweets
        #我follow的人的tweets
        #这里的followers是上面那张follower|followed的关系表
        followed = Tweet.query.join(
            followers, (followers.c.follower_id == self.id)).filter(
                Tweet.user_id == followers.c.followed_id
            )
        #两张表join在一起
        return followed.union(own).order_by(Tweet.create_time.desc())        
    
    def get_jwt(self, expire = 7200):
        return jwt.encode(
            {
                'email' : self.email,
                'exp': time.time() + expire #time limit
            },
            current_app.config['SECRET_KEY'],
            algorithm = 'HS256'
        ).decode('utf-8')
        #如果不decode,产生的会是一个binary string
    
    
    #做成一个静态的方法,因为我们不希望使用的时候还需要去实例化一个user对象\
    #一般来说，要使用某个类的方法，需要先实例化一个对象再调用方法。\
    #而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。\
    #这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。\
    #因为我们可以去route里面看到: user : User.verify_jwt(token)\
    #这时候我们是通过User这个class去调用的这个方法,而我们并不知道是哪一个用户,我们只能通过verify这个方法\
    #去帮我们返回User.query.filter_by(email = email).first 用户的实力\
    @staticmethod
    def verify_jwt(token):
        try:
            email = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms = 'HS256'
            )
            email = email['email']
        except:
            return
        return User.query.filter_by(email = email).first()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))