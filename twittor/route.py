from flask import render_template, abort
"""abort: 这是返回404的"""
from twittor.forms import LoginForm, RegisterForm, EditProfileForm, TweetForm, \
    PasswordResetRequestForm, PasswordResetForm
from flask import redirect
from flask import url_for, request, current_app, flash
"""每次在models里面有新加了class之后，要在这里更新一下，让route知道我们做了什么。"""
from flask_login import login_user, current_user, logout_user, login_required
from twittor import db
from twittor.email import send_async_mail, send_email
from twittor.models.user import User, load_user
from twittor.models.tweet import Tweet


@login_required
def index():
    #name = {'username' : current_user.username}
    form = TweetForm()
    if form.validate_on_submit():
        t = Tweet(body = form.tweet.data, author = current_user)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    page_num = int(request.args.get('page') or 1)#这里我就能知道我当前是第几页然后我们就能根据当前的page index 来翻页
    tweets = current_user.own_and_followed_tweets().paginate(
        page = page_num, per_page = current_app.config['TWEET_PER_PAGE'], error_out = False)
    #这里tweets是一个page的对象,里面有next num,然后显示在网页上的是tweets.items
    if tweets.has_next:
        next_url = url_for('index', page = tweets.next_num)
    else:
        next_url = None
    if tweets.has_prev:
        prev_url = url_for('index', page = tweets.prev_num)
    else:
        prev_url = None
    return render_template(
        'index.html', tweets = tweets.items, form = form, next_url = next_url, prev_url = prev_url)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username = form.username.data).first()
        """null or the only one as the username is unique"""
        if u is None or not u.check_password(form.password.data):
            print('Invalid username or Incorrect password')
            return redirect(url_for('login'))
        login_user(u, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title = "Sign in", form = form)


def logout():
    logout_user()
    return redirect(url_for('login'))

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title = "Registration", form = form)


@login_required
def user(username):
    u = User.query.filter_by(username = username).first()
    if u is None:
        abort(404)
    #因为我们有了一个db relation表,backref = "author"
    if request.method == "POST":
        if request.form['request_button'] == 'Follow':
            current_user.follow(u)
            db.session.commit()
        elif request.form['request_button'] == 'Unfollow':
            current_user.unfollow(u)
            db.session.commit()
        else:
            flash("Send an email to your email address, please check you email")
            send_email_for_user_activate(current_user)
    page_num = int(request.args.get('page') or 1)
    tweets = u.tweets.order_by(Tweet.create_time.desc()).paginate(
        page = page_num, per_page = current_app.config['TWEET_PER_PAGE_USER'], error_out = False)
    if tweets.has_prev:
        prev_url = url_for('profile', username = u.username, page = tweets.prev_num)
    else:
        prev_url = None
    if tweets.has_next:
        next_url = url_for('profile', username = u.username, page = tweets.next_num)
    else:
        next_url = None
    return render_template('/user.html', title = "Profile", 
        user = u, tweets = tweets.items, prev_url = prev_url, next_url = next_url
    )

def send_email_for_user_activate(user):
    token = user.get_jwt()
    url_user_activate = url_for(
        'user_activate',
        token = token,
        _external = True
    )
    send_email(
        subject = current_app.config['MAIN_SUBJECT_USER_ACTIVATE'],
        recipients = [user.email],
        text_body = render_template(
            'email/user_activate.txt',
            username = user.username,
            url_user_activate = url_user_activate
        ),
        html_body = render_template(
            'email/user_activate.txt',
            username = user.username,
            url_user_activate = url_user_activate
        )
    )

def user_activate(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_jwt(token)
    if not user:
        msg = "Token has expired, please try to re-send email."
    else:
        user.is_activated = True
        db.session.commit()
        msg = 'User has been activated!'
    return render_template('user_activated.html', msg = msg)


def page_not_found(e):
    return render_template('/404.html'), 404
    """不加这个e和404会报错."""

@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'GET':
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        """这里页面跳转非常tricky 需要时profile 然后给另外一个参数 username,由于我们已经import了
        current_user.username 来作为username传入.
        """
        return redirect(url_for('profile', username = current_user.username))
    return render_template('/edit_profile.html', form = form)

def reset_password_request():
    if current_user.is_authenticated:
        #已经登陆了 不需要重置密码了
        return redirect (url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(
                "You will receive an email allowing you to reset your \
                    password. Please check your trash or spam if you could not find it."
            )
            #send email in this block#
            token = user.get_jwt()
            url = 'http://127.0.0.1:5000/password_reset/{}'.format(token)
            send_email(
                subject = '[Twittor] Reset your password',
                recipients = [user.email],
                text_body = "please click this link to reset your password, \
                            please do not share this link with anyone. {}".format(url),
                html_body = '<h5> please click this link to reset your password, \
                            please do not share this link with anyone. {}</h5>'.format(url)
            )
        return redirect(url_for('login'))
    return render_template('password_reset_request.html', form = form)

def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #用jwt来decode的email!
    user = User.verify_jwt(token)
    if not user:
        return redirect(url_for('login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('password_reset.html', title = 'Password Reset', form = form)

@login_required
def explore():
    page_num = int(request.args.get('page') or 1)
    tweets = Tweet.query.order_by(Tweet.create_time.desc()).paginate(
        page = page_num , per_page = current_app.config['TWEET_PER_PAGE'], error_out = False
    )

    next_url = url_for('index', page = tweets.next_num) if tweets.has_next else None
    prev_url = url_for('index', page = tweets.prev_num) if tweets.has_prev else None
    return render_template('explore.html', tweets = tweets.items, next_url = next_url, prev_url = prev_url)