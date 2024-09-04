from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import StudentRegistrationForm, ReportMissingResultsForm
from app.models import Student, Course

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        student = Student(student_id=form.student_id.data, name=form.name.data, email=form.email.data)
        db.session.add(student)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('student_registration.html', form=form)

@app.route('/report_missing_results', methods=['GET', 'POST'])
def report_missing_results():
    form = ReportMissingResultsForm()
    if form.validate_on_submit():
        # Handle the missing result report logic here
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('report_missing_results.html', form=form)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Admin logic to view and manage student registrations
    return render_template('admin_dashboard.html')