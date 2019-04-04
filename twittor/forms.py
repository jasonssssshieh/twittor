from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from twittor.models.user import User

class LoginForm(FlaskForm):
    class Meta:
        csrf = False #去掉一直出来的警告:/Users/Jason/Desktop/flask-demo/twittor/route.py:23: 
        #FlaskWTFDeprecationWarning: "csrf_enabled" 
        #is deprecated and will be removed in 1.0. Set "meta.csrf" instead.
    username = StringField(label = "Username", validators=[DataRequired()])
    password = PasswordField(label = "Password", validators=[DataRequired()])
    remember_me = BooleanField(label = "Remember me")
    submit = SubmitField(label = "Sign In")

class RegisterForm(FlaskForm):
    username = StringField(label = "Username", validators=[DataRequired()])
    email = StringField(label = "Email Address", validators = [DataRequired(), Email()])
    password = PasswordField(label = "Password", validators=[DataRequired()])
    password2 = PasswordField(label = "Password Repeat", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            print('Duplicate username!!')
            raise ValidationError(
                "This usename has been occupied, please use a different username")
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            print('Duplicate email!!')
            raise ValidationError(
                "This email address has been occupied, please use a different email address")

class EditProfileForm(FlaskForm):
    about_me = TextAreaField(label = 'About me', validators=[Length(min = 0, max = 256)])
    submit = SubmitField('Save')


class TweetForm(FlaskForm):
    tweet = TextAreaField(label = 'Tweet', validators=[DataRequired(), Length(min = 1, max = 140)])
    submit = SubmitField('Tweet')

class PasswordResetRequestForm(FlaskForm):
    email = StringField(label = "Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField(label = "Reset Password")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError("The email address does not exist!")

class PasswordResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Your Pass", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Reset')