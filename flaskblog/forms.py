from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    title = StringField('Pastor,SYL,MG, Pathfinder,Adventurer')
    full_name = StringField('Full Name',validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[InputRequired()])
    church = StringField('Your Church',validators=[DataRequired(), Length(min=2, max=100)])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PastorForm(FlaskForm):
    name = StringField('Name of the Pastor', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[InputRequired()])
    wife = StringField('Name of his wife', validators=[DataRequired()])
    picture = FileField('His Picture', validators=[FileAllowed(['jpg', 'png'])])
    wife_picture = FileField('His wife Picture', validators=[FileAllowed(['jpg', 'png'])])
    bio = TextAreaField('Biolography', validators=[DataRequired()])
    submit = SubmitField('Register')

class ChurchForm(FlaskForm):
    name = StringField('Name of the Church', validators=[DataRequired()])
    est = DateField('Date of Birth', validators=[InputRequired()])
    loc = StringField('Location of the Church', validators=[DataRequired()])
    picture = FileField('Church Picture', validators=[FileAllowed(['jpg', 'png'])])
    members = IntegerField('Number of Members',validators =[DataRequired()])
    submit = SubmitField('Register')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Blog Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class SermonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    message = TextAreaField('Content', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    picture = FileField('Sermon Picture', validators=[FileAllowed(['jpg', 'png'])])
    video = FileField('Sermon Video', validators=[FileAllowed(['mp4', 'mpeg','mkv'])])
    submit = SubmitField('Upload')

class UpEventForm(FlaskForm):
    event = StringField('The Event', validators=[DataRequired()])
    start_time = DateField('Start Time', validators=[DataRequired()])
    end_time = DateField('End Time', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    facilitator = StringField('The Facilatator', validators=[DataRequired()])
    picture = FileField('Event Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class DonationForm(FlaskForm):
    title = StringField('The title', validators=[DataRequired()])
    target = IntegerField('Target',validators =[DataRequired()])
    received = IntegerField('Received',validators =[DataRequired()])
    message = TextAreaField('About What')
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

class QuoteForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    message = TextAreaField('Quote')
    ref = StringField('Reference', validators=[DataRequired()])
    submit = SubmitField('Post')

class PastProgramForm(FlaskForm):
    program = StringField('Program', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class CommentForm(FlaskForm):
    email = StringField('Email * ')
    message = TextAreaField('Message * ')
    submit = SubmitField('Post Comment')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
