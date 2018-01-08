from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    subreddit = StringField('Subreddit', validators=[DataRequired()])
    thread = StringField('Thread Name', validators=[DataRequired()])
    postAuthor = StringField('Thread Author', validators=[DataRequired()])
    searchTerm = StringField('Search Term', validators=[DataRequired()])
    searchNumber = IntegerField('Number threads searched', validators=[DataRequired()])
    submit = SubmitField('Search')
