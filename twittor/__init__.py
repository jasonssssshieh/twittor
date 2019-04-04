from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from twittor.config import Config
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
"""
先有了db，然后再去初始化，否则我们引入route的时候，route里面会importmodels的user， 
而这个models又会import db
所以这里在创建了db之后再import route的index and login
"""
login_manager = LoginManager()
login_manager.login_view = 'login'#强制用户登陆
mail = Mail() #初始化一个mail对象  用于发送邮件


from twittor.route import index, login, logout, register, user, \
     page_not_found, edit_profile, reset_password_request, password_reset, \
         explore, user_activate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:twittor.db:"
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/demo"
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)#log in和app就做了一个关联
    mail.init_app(app)
    app.add_url_rule('/', 'index', index, methods = ['GET', 'POST'])
    app.add_url_rule('/index', 'index', index, methods = ['GET', 'POST'])
    app.add_url_rule('/login', 'login', login, methods = ['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods = ['GET', 'POST'])
    app.add_url_rule('/<username>', 'profile', user, methods = ['GET', 'POST'])
    app.add_url_rule('/edit_profile', 'edit_profile', edit_profile, methods = ['GET', 'POST'])
    app.add_url_rule('/reset_password_request', 'reset_password_request', reset_password_request, methods = ["GET", "POST"])
    app.add_url_rule('/password_reset/<token>', 'password_reset', password_reset, methods = ['GET', 'POST'])
    app.add_url_rule('/explore', 'explore', explore, methods = ['GET', 'POST'])
    app.add_url_rule('/activate/<token>', 'user_activate', user_activate)
    app.register_error_handler(404, page_not_found)
    return app

