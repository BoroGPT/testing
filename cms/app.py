from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DATA_FILE = Path(__file__).parent / 'classes.json'


def load_data():
    """Load classes data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"classes": []}


def save_data(data):
    """Save classes data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_class(data, class_id):
    """Get a class by ID"""
    for cls in data['classes']:
        if cls['id'] == class_id:
            return cls
    return None


@app.route('/')
def index():
    """Home page - list all classes"""
    data = load_data()
    return render_template('index.html', classes=data['classes'])


@app.route('/class/<class_id>')
def view_class(class_id):
    """View detailed class information"""
    data = load_data()
    cls = get_class(data, class_id)
    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))
    return render_template('class_detail.html', cls=cls)


@app.route('/class/add', methods=['GET', 'POST'])
def add_class():
    """Add a new class"""
    if request.method == 'POST':
        data = load_data()

        class_id = request.form.get('class_id')
        name = request.form.get('name')
        instructor = request.form.get('instructor')
        schedule = request.form.get('schedule')
        room = request.form.get('room')

        if get_class(data, class_id):
            flash(f'Class with ID "{class_id}" already exists', 'error')
            return redirect(url_for('add_class'))

        new_class = {
            "id": class_id,
            "name": name,
            "instructor": instructor,
            "schedule": schedule,
            "room": room,
            "students": [],
            "assignments": []
        }

        data['classes'].append(new_class)
        save_data(data)
        flash(f'Class "{name}" added successfully', 'success')
        return redirect(url_for('view_class', class_id=class_id))

    return render_template('add_class.html')


@app.route('/class/<class_id>/edit', methods=['GET', 'POST'])
def edit_class(class_id):
    """Edit class information"""
    data = load_data()
    cls = get_class(data, class_id)

    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        cls['name'] = request.form.get('name')
        cls['instructor'] = request.form.get('instructor')
        cls['schedule'] = request.form.get('schedule')
        cls['room'] = request.form.get('room')

        save_data(data)
        flash('Class updated successfully', 'success')
        return redirect(url_for('view_class', class_id=class_id))

    return render_template('edit_class.html', cls=cls)


@app.route('/class/<class_id>/delete', methods=['POST'])
def delete_class(class_id):
    """Delete a class"""
    data = load_data()
    data['classes'] = [c for c in data['classes'] if c['id'] != class_id]
    save_data(data)
    flash('Class deleted successfully', 'success')
    return redirect(url_for('index'))


@app.route('/class/<class_id>/student/add', methods=['GET', 'POST'])
def add_student(class_id):
    """Add a student to a class"""
    data = load_data()
    cls = get_class(data, class_id)

    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        name = request.form.get('name')
        email = request.form.get('email')

        # Check if student already exists
        if any(s['id'] == student_id for s in cls['students']):
            flash(f'Student "{student_id}" already enrolled in this class', 'error')
            return redirect(url_for('add_student', class_id=class_id))

        new_student = {
            "id": student_id,
            "name": name,
            "email": email
        }

        cls['students'].append(new_student)
        save_data(data)
        flash(f'Student "{name}" added successfully', 'success')
        return redirect(url_for('view_class', class_id=class_id))

    return render_template('add_student.html', cls=cls)


@app.route('/class/<class_id>/student/<student_id>/delete', methods=['POST'])
def delete_student(class_id, student_id):
    """Remove a student from a class"""
    data = load_data()
    cls = get_class(data, class_id)

    if cls:
        cls['students'] = [s for s in cls['students'] if s['id'] != student_id]
        # Also remove their grades
        for assignment in cls['assignments']:
            if student_id in assignment['grades']:
                del assignment['grades'][student_id]
        save_data(data)
        flash('Student removed successfully', 'success')

    return redirect(url_for('view_class', class_id=class_id))


@app.route('/class/<class_id>/assignment/add', methods=['GET', 'POST'])
def add_assignment(class_id):
    """Add an assignment to a class"""
    data = load_data()
    cls = get_class(data, class_id)

    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        assignment_id = request.form.get('assignment_id')
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        max_points = request.form.get('max_points')

        # Check if assignment already exists
        if any(a['id'] == assignment_id for a in cls['assignments']):
            flash(f'Assignment "{assignment_id}" already exists in this class', 'error')
            return redirect(url_for('add_assignment', class_id=class_id))

        new_assignment = {
            "id": assignment_id,
            "title": title,
            "due_date": due_date,
            "max_points": int(max_points),
            "grades": {}
        }

        cls['assignments'].append(new_assignment)
        save_data(data)
        flash(f'Assignment "{title}" added successfully', 'success')
        return redirect(url_for('view_class', class_id=class_id))

    return render_template('add_assignment.html', cls=cls)


@app.route('/class/<class_id>/assignment/<assignment_id>/delete', methods=['POST'])
def delete_assignment(class_id, assignment_id):
    """Delete an assignment"""
    data = load_data()
    cls = get_class(data, class_id)

    if cls:
        cls['assignments'] = [a for a in cls['assignments'] if a['id'] != assignment_id]
        save_data(data)
        flash('Assignment deleted successfully', 'success')

    return redirect(url_for('view_class', class_id=class_id))


@app.route('/class/<class_id>/grades', methods=['GET', 'POST'])
def manage_grades(class_id):
    """Manage grades for a class"""
    data = load_data()
    cls = get_class(data, class_id)

    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        assignment_id = request.form.get('assignment_id')
        student_id = request.form.get('student_id')
        grade = request.form.get('grade')

        # Find assignment
        assignment = next((a for a in cls['assignments'] if a['id'] == assignment_id), None)

        if assignment:
            try:
                grade_value = float(grade)
                if 0 <= grade_value <= assignment['max_points']:
                    assignment['grades'][student_id] = grade_value
                    save_data(data)
                    flash('Grade recorded successfully', 'success')
                else:
                    flash(f'Grade must be between 0 and {assignment["max_points"]}', 'error')
            except ValueError:
                flash('Invalid grade value', 'error')

        return redirect(url_for('manage_grades', class_id=class_id))

    return render_template('manage_grades.html', cls=cls)


@app.route('/class/<class_id>/student/<student_id>/report')
def student_report(class_id, student_id):
    """Generate a report for a student"""
    data = load_data()
    cls = get_class(data, class_id)

    if not cls:
        flash('Class not found', 'error')
        return redirect(url_for('index'))

    student = next((s for s in cls['students'] if s['id'] == student_id), None)

    if not student:
        flash('Student not found', 'error')
        return redirect(url_for('view_class', class_id=class_id))

    # Calculate grades
    total_points = 0
    earned_points = 0
    assignment_details = []

    for assignment in cls['assignments']:
        assignment_info = {
            'title': assignment['title'],
            'due_date': assignment['due_date'],
            'max_points': assignment['max_points'],
            'grade': assignment['grades'].get(student_id),
            'percentage': None
        }

        total_points += assignment['max_points']

        if student_id in assignment['grades']:
            grade = assignment['grades'][student_id]
            earned_points += grade
            assignment_info['percentage'] = (grade / assignment['max_points']) * 100

        assignment_details.append(assignment_info)

    overall_percentage = (earned_points / total_points * 100) if total_points > 0 else 0

    return render_template('student_report.html',
                         cls=cls,
                         student=student,
                         assignments=assignment_details,
                         total_points=total_points,
                         earned_points=earned_points,
                         overall_percentage=overall_percentage)


@app.route('/search')
def search():
    """Search for classes, students, or instructors"""
    query = request.args.get('q', '').lower()

    if not query:
        return redirect(url_for('index'))

    data = load_data()
    results = []

    for cls in data['classes']:
        # Search in class name, ID, instructor
        if (query in cls['name'].lower() or
            query in cls['id'].lower() or
            query in cls['instructor'].lower()):
            results.append({
                'type': 'class',
                'class': cls,
                'student': None
            })

        # Search in students
        for student in cls['students']:
            if (query in student['name'].lower() or
                query in student['id'].lower() or
                query in student['email'].lower()):
                results.append({
                    'type': 'student',
                    'class': cls,
                    'student': student
                })

    return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
