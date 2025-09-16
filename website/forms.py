from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=150)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=150)])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], 
                          widget=TextArea(), render_kw={"rows": 10})
    category = SelectField('Category', choices=[
        ('General', 'General'),
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Ideas', 'Ideas'),
        ('Learning', 'Learning'),
        ('Projects', 'Projects')
    ], default='General')
    tags = StringField('Tags (comma-separated)', validators=[Optional()])
    is_favorite = BooleanField('Mark as Favorite')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('General', 'General'),
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('Ideas', 'Ideas'),
        ('Learning', 'Learning'),
        ('Projects', 'Projects')
    ], default='')
    show_favorites_only = BooleanField('Favorites Only')
