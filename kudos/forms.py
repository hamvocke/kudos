from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectMultipleField, RadioField
from wtforms.validators import required, optional, Length, Email


class CreateFeedbackForm(FlaskForm):
    name = StringField('Title', validators=[required(), Length(max=150)])
    description = TextAreaField('Description', validators=[optional(), Length(max=1000)])
    email = StringField('E-Mail', validators=[optional(), Email()])
    options = SelectMultipleField('Answers', coerce=int, validators=[required()])
    submit = SubmitField('Create Feedback')


class VoteForm(FlaskForm):
    text = TextAreaField('Description', validators=[optional(), Length(max=1000)])
    option = RadioField('Option', coerce=int, validators=[required()])
    submit = SubmitField('Give Feedback')