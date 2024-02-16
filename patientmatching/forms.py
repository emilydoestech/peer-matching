from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

class CreateProfileForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    symptoms = StringField('Symptoms (separated by commas)', validators=[DataRequired(), Length(min=2, max=100)])
    diagnosis = BooleanField('Only see people with a diagnosis')
    number = IntegerField('How many people do you want to be matched with', validators=[DataRequired(), NumberRange(min=1, max=12)])
    submit = SubmitField('Find Matches')

class EditProfileForm(FlaskForm):
    newSymptoms = StringField('Symptoms (separated by commas)', validators=[Length(max=100)])
    submit_edit_form = SubmitField('Update Matches')

class DiagnosisForm(FlaskForm):
    diagnosis_true = SubmitField('Only see diagnosed matches')
    diagnosis_false = SubmitField('See top matches')
