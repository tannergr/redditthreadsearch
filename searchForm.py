from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    subreddit = StringField('Subreddit', validators=[DataRequired()], default="cscareerquestions")
    thread = StringField('Thread Name', validators=[DataRequired()], default="Daily Chat")
    postAuthor = StringField('Thread Author', validators=[DataRequired()], default="AutoModerator")
    searchTerm = StringField('Search Term', validators=[DataRequired()], default="Interview")
    searchNumber = IntegerField('Number threads searched', validators=[DataRequired()], default="5")
    submit = SubmitField('Search')
