"""
把配置文件全部放在create app里面不是一个好的选择，因此，这里建立一个
"""
import os 
"""获取当前config文件的路径，"""
config_path = os.path.abspath(os.path.dirname(__file__))


"""
引入环境变量
"""
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, 'twittor.db'))
    #"sqlite:///" + os.path.join(config_path, 'twittor.db')
    #"sqlite:///:twittor.db:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'abc123')
    TWEET_PER_PAGE = os.environ.get('TWEET_PER_PAGE', 10)
    TWEET_PER_PAGE_USER = os.environ.get('TWEET_PER_PAGE_USER', 10)

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER','noreply@twittor.com')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 1)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'twittor.service')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'A4328902b')
    MAIL_SUBJECT_RESET_REQUEST = '[Twittor] Please Reset Your Password'
    MAIN_SUBJECT_USER_ACTIVATE = '[Twittor] Please Activate Your Account'
    