from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    program = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    students = db.relationship('Student', secondary='registrations')

class Registration(db.Model):
    __tablename__ = 'registrations'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade = db.Column(db.String(2), nullable=False)
    semester = db.Column(db.String(20), nullable=False)

# Forms
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    program = SelectField('Program', choices=[('Computer Science', 'Computer Science'),
                                              ('Business Administration', 'Business Administration'),
                                              ('Engineering', 'Engineering'),
                                              ('Mathematics', 'Mathematics'),
                                              ('Literature', 'Literature')], 
                          validators=[DataRequired()])
    
    course_name = FieldList(StringField('Course Name', validators=[DataRequired()]), min_entries=1)
    course_code = FieldList(StringField('Course Code', validators=[DataRequired()]), min_entries=1)
    
    submit = SubmitField('Register')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data, program=form.program.data)
        db.session.add(student)
        db.session.commit()

        # Save the course registration
        for course_name, course_code in zip(form.course_name.data, form.course_code.data):
            course = Course.query.filter_by(course_name=course_name, course_code=course_code).first()
            if not course:
                course = Course(course_name=course_name, course_code=course_code)
                db.session.add(course)
                db.session.commit()
            registration = Registration(student_id=student.id, course_id=course.id)
            db.session.add(registration)
            db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('student/registration.html', form=form)

@app.route('/student/results', methods=['GET', 'POST'])
def view_results():
    if request.method == 'POST':
        semester = request.form.get('semester')
        student_id = 1  # Assume logged-in student ID for now
        results = Result.query.filter_by(student_id=student_id, semester=semester).all()
        return render_template('student/view_results.html', results=results, selected_semester=semester)

    return render_template('student/view_results.html', results=[], selected_semester=None)

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/reports')
def admin_reports():
    report_data = {
        'programs': ['Computer Science', 'Business', 'Engineering', 'Mathematics', 'Literature'],
        'passed': [150, 120, 180, 100, 90],
        'failed': [20, 10, 30, 15, 25]
    }
    return render_template('admin/reports.html', report_data=report_data)

@app.route('/admin/manage_registrations')
def manage_registrations():
    registrations = Registration.query.all()
    return render_template('admin/manage_registrations.html', registrations=registrations)

@app.route('/admin/delete_registration/<int:student_id>/<int:course_id>', methods=['POST'])
def delete_registration(student_id, course_id):
    registration = Registration.query.filter_by(student_id=student_id, course_id=course_id).first()
    if registration:
        db.session.delete(registration)
        db.session.commit()
        flash('Registration deleted successfully!', 'success')
    else:
        flash('Registration not found!', 'error')
    
    return redirect(url_for('manage_registrations'))

@app.route('/admin/statistics')
def admin_statistics():
    total_students = Student.query.count()
    total_courses = Course.query.count()
    registrations_count = Registration.query.count()

    # Additional statistics can be calculated here
    return render_template('admin/statistics.html', 
                           total_students=total_students, 
                           total_courses=total_courses, 
                           registrations_count=registrations_count)

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)