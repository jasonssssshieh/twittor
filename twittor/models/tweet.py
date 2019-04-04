#专门用来定义数据库

from datetime import datetime
from twittor import db




#开头我们import了log in,也就是在init里面的那个loginManger的对象
#login_manager.user_loader#作为一个装饰器去装饰我们的load_user
#这里需要一个user_loader的这样的一个回调函数:
#is used to reload the user object from the user ID stored in the session


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    """ 这里user是小写，代表table的名字，而这个class是大写的User
        默认情况下table的名字就是小写的class
    """

    def __repr__(self):
        return 'id = {}, body = {}, create at {}, user_id = {}'.format(
            self.id, self.body, self.create_time, self.user_id
        )