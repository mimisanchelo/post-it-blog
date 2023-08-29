from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, URL
from flask_ckeditor import CKEditorField



class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 40)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 100)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    content = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class UserForm(FlaskForm):
    name = StringField('Name', validators=[])
    username = StringField('Username', validators=[Length(1, 40)])
    bio = CKEditorField('Bio', validators=[Length(0, 120)])
    img_url = StringField("Profile Image", validators=[URL()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
