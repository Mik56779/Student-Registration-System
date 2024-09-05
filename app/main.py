from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy credentials for admin and students
admin_credentials = {'username': 'admin', 'password': 'admin123'}
students = {
    '20230001': {'password': 'student123', 'name': 'Alice Smith', 'email': 'alice.smith@example.com', 'program': 'Computer Science', 'year': '3rd Year', 'semester': '1', 'results': [{'course_code': 'CSE101', 'course_name': 'Introduction to Programming', 'grade': 'A'}, {'course_code': 'CSE102', 'course_name': 'Data Structures', 'grade': 'B+'}]},
    '20230002': {'password': 'student456', 'name': 'Bob Johnson', 'email': 'bob.johnson@example.com', 'program': 'Electrical Engineering', 'year': '2nd Year', 'semester': '2', 'results': [{'course_code': 'EEE101', 'course_name': 'Circuit Analysis', 'grade': 'B'}, {'course_code': 'EEE102', 'course_name': 'Electromagnetics', 'grade': 'A-'}]}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Username or Password")
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        if student_id in students and students[student_id]['password'] == password:
            return redirect(url_for('student_dashboard', student_id=student_id))
        else:
            flash("Invalid Student ID or Password")
            return redirect(url_for('student_login'))
    return render_template('student_login.html')

@app.route('/register_student', methods=['POST'])
def register_student():
    program = request.form.get('program')
    course = request.form.get('course')
    year = request.form.get('year')
    semester = request.form.get('semester')

    # Process the registration data (e.g., store it in a database or perform further actions)
    student_id = '12345'  # You should replace this with actual logic to generate or fetch student_id
    # Flash a success message and redirect to the student dashboard
    flash("Registration successful!")
    return redirect(url_for('student_dashboard', student_id=student_id))

@app.route('/student_results/<student_id>')
def student_results(student_id):
    student = students.get(student_id)
    if not student:
        flash("Student not found")
        return redirect(url_for('student_login'))
    results = student.get('results', [])
    return render_template('student_results.html', results=results, student_id=student_id)

@app.route('/student_profile/<student_id>')
def student_profile(student_id):
    student = students.get(student_id)
    if not student:
        flash("Student not found")
        return redirect(url_for('student_login'))
    return render_template('student_profile.html', student=student)

@app.route('/student/dashboard/<student_id>')
def student_dashboard(student_id):
    student = students.get(student_id)
    if not student:
        flash("Student not found")
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html', student_id=student_id, student=student)

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/student/dashboard/registration')
def std_reg():
    return render_template('student_registration.html')

if __name__ == '__main__':
    app.run(debug=True)