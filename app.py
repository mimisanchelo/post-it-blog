from flask import Flask, render_template, redirect, flash, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor

from datetime import datetime as dt
from forms import LoginForm, SignupForm, PostForm, UserForm, SearchForm, CommentForm

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECREK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    bio = db.Column(db.String(120), nullable=True)
    img_url = db.Column(db.String(400), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable=False)
    date_joined = db.Column(db.DateTime, default=dt.now())

    # Relationships
    posts = db.relationship('Post', backref='poster' , cascade="all, delete-orphan")
    comment = db.relationship('Comment', backref='Commenter', cascade="all, delete-orphan")
    ## Like btn
    liked = db.relationship('Social_like',
                            foreign_keys='Social_like.user_id', 
                            backref='user_like', lazy='dynamic', 
                            cascade="all, delete-orphan")

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = Social_like(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            Social_like.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return Social_like.query.filter(
            Social_like.user_id == self.id,
            Social_like.post_id == post.id).count() > 0
    
    ## Follow btn
    followed = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    
    followers = db.relationship('Follow',
                              foreign_keys='Follow.followed_id',
                              backref=db.backref('followed', lazy='joined'),
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    
    def follow(self, user):
        if not self.is_following(user):
            person = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(person)

    def unfollow(self, user):
        if self.is_following(user):
            Follow.query.filter_by(
                follower_id=self.id, 
                followed_id=user.id).delete()

    def is_following(self, user):
        return Follow.query.filter(
            Follow.follower_id == self.id,
            Follow.followed_id == user.id).count() > 0

    def get_following(self, user):
        return Follow.query.filter(
            Follow.followed_id == user.id).count()
    
    def get_follower(self, user):
        return Follow.query.filter(
            Follow.follower_id == user.id).count()    
    
   
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable = False)
    content = db.Column(db.Text)
    img_url = db.Column(db.String(400), nullable=False)
    # author = db.Column(db.String(250), nullable=False)
    date_posted = db.Column(db.DateTime, default=dt.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='parent_post', cascade="all, delete-orphan")
    likes = db.relationship('Social_like', backref='post', lazy='dynamic', cascade="all, delete-orphan")
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    date_commented = db.Column(db.DateTime, default=dt.now())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

class Social_like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    date_follow = db.Column(db.DateTime, default=dt.now())


with app.app_context():
    db.create_all()

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

#------------ ACTIONS ---------------#
@app.route('/like/<int:post_id>/<action>')
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()

    if action =='like':
        current_user.like_post(post)
        db.session.commit()

    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()

    return redirect(request.referrer)

@app.route('/follow/<int:user_id>/<action>')
@login_required
def follow_action(user_id, action):
    user = User.query.filter_by(id=user_id).first_or_404()
    if action =='follow':
        current_user.follow(user)
        db.session.commit()

    if action == 'unfollow':
        current_user.unfollow(user)
        db.session.commit()

    return redirect(request.referrer)

#------------ SEARCH RESULT ---------------#
@app.route('/search', methods=['GET', 'POST'])
def get_search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        # query db
        posts = posts.filter(Post.content.like('%' + post_searched + '%') | 
                            Post.title.like('%' + post_searched + '%'))
        posts = posts.order_by(Post.date_posted.desc()).all()
    

        return render_template('search.html', 
                               form=form, 
                               searched = post_searched,
                               posts=posts
                            )

#------------ PROFILE ---------------#
@app.route('/profile/settings/<int:id>', methods=['GET', 'POST'])
@login_required
def profile_settings(id):
    profile_to_update = User.query.get_or_404(id)
    form = UserForm(
        obj = profile_to_update
    )
    if request.method == 'POST':
        profile_to_update.name = request.form['name']
        profile_to_update.username = request.form['username']
        profile_to_update.bio = request.form['bio']


        if request.form['img_url'] == '':
            profile_to_update.img_url = profile_to_update.img_url
        else:
            profile_to_update.img_url = request.form['img_url']


        try:
            db.session.commit()
            return redirect(url_for("profile", id=profile_to_update.id))
        except:
            flash('You have done something wrong. Try again!')
    return render_template('profile/settings.html', form=form)


@app.route('/profile/<path:id>')
@login_required
def profile(id):
    user = User.query.get(id)
    print(user)
    return render_template('profile/profile.html', user=user)

#------------ POST ---------------#
@app.route('/delete/<int:id>')
def delete_post(id):
    post = Post.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()

        flash('Post has been deleted!')

        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('index.html', posts=posts)
    except:
        flash('Something went wrong. Try again!')

@app.route('/show_post/edit/<int:id>', methods=['GET', "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(
        obj=post
    )
    if form.validate_on_submit():
        post.title= form.title.data
        post.content = form.content.data
        post.img_url = form.img_url.data

        try:
            db.session.commit()
            return redirect(url_for("show_post", id=post.id))
        except:
            flash('Something went wrong!')
    return render_template('post/edit-post.html', form=form)

@app.route('/show_post/<int:id>', methods=['GET', 'POST'])
def show_post(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('You need to login or register to comment')
            return redirect(url_for('login'))
        
        new_comment = Comment(
            text = form.content.data,
            author_id = current_user.id,
            parent_post = post
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', id=post.id))

    return render_template('post/show-post.html', post=post, form=form)


@app.route("/delete-comment/<post_id>/<comment_id>")
@login_required
def delete_comment(comment_id, post_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('show_post', id=post_id))


@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            img_url = form.img_url.data,
            author_id = poster)
        
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('profile', id=current_user.id))
   
    return render_template('post/create-post.html', form=form)

#------------ REGISTRATION ---------------#
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        new_user = User.query.filter_by(email=form.email.data).first()
        if new_user is None:
            if form.password.data == form.password2.data:

                hash_password = generate_password_hash(form.password.data)
                
                new_user = User(
                    email = form.email.data,
                    password = hash_password,
                    name = form.name.data,
                    username = form.username.data,
                )
                
                db.session.add(new_user)
                db.session.commit()
                flash('Signed Up successfully! Time to Log In')
                return redirect('login')
            else:
                flash('Passwords must match!')
        else:
            flash('An account is already registered with your email')
        form.name.data = ''
        form.email.data = ''
        form.username.data = ''
        form.password.data = ''
        form.password2.data = ''
        
    return render_template('auth/signup.html', form=form)
        
#------------ AUTHENTICATION ---------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('profile', id=user.id))
            else:
                flash('Wrong password')
        else:
            flash('That user doesn`t exist')
    return render_template('auth/login.html', form=form)

#------------ LOGOUT ---------------#
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!")
    return redirect(url_for('login'))

#------------ HOME PAGE (FEED) ---------------#
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)