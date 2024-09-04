from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email

class StudentRegistrationForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class ReportMissingResultsForm(FlaskForm):
    course_id = StringField('Course ID', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired()])
    exam_date = StringField('Date of Exam', validators=[DataRequired()])
    description = TextAreaField('Description of the Issue')
    submit = SubmitField('Report')