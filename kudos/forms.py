from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Email


class CreateFeedbackForm(FlaskForm):
    name = StringField('What are you collecting feedback for?', validators=[DataRequired(), Length(max=150)])
    email = StringField('What is your email address?', validators=[DataRequired(), Email()])
