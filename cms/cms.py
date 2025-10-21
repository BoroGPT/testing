import json
import argparse
from pathlib import Path
from datetime import datetime


class ClassCMS:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Load classes data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"classes": []}

    def save_data(self):
        """Save classes data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def list_classes(self):
        """List all classes"""
        if not self.data['classes']:
            print("No classes found.")
            return

        print(f"\n{'ID':<10} {'Name':<40} {'Instructor':<25} {'Schedule':<20}")
        print("-" * 95)
        for cls in self.data['classes']:
            print(f"{cls['id']:<10} {cls['name']:<40} {cls['instructor']:<25} {cls['schedule']:<20}")
        print()

    def get_class(self, class_id):
        """Get a class by ID"""
        for cls in self.data['classes']:
            if cls['id'] == class_id:
                return cls
        return None

    def view_class(self, class_id):
        """View detailed information about a class"""
        cls = self.get_class(class_id)
        if not cls:
            print(f"Class '{class_id}' not found.")
            return

        print(f"\nClass: {cls['name']}")
        print(f"ID: {cls['id']}")
        print(f"Instructor: {cls['instructor']}")
        print(f"Schedule: {cls['schedule']}")
        print(f"Room: {cls['room']}")

        print(f"\nStudents ({len(cls['students'])}):")
        for student in cls['students']:
            print(f"  - {student['name']} ({student['id']}) - {student['email']}")

        print(f"\nAssignments ({len(cls['assignments'])}):")
        for assignment in cls['assignments']:
            print(f"  - {assignment['title']} (ID: {assignment['id']})")
            print(f"    Due: {assignment['due_date']} | Max Points: {assignment['max_points']}")
            print(f"    Graded: {len(assignment['grades'])}/{len(cls['students'])} students")
        print()

    def add_class(self, class_id, name, instructor, schedule, room):
        """Add a new class"""
        if self.get_class(class_id):
            print(f"Class with ID '{class_id}' already exists.")
            return False

        new_class = {
            "id": class_id,
            "name": name,
            "instructor": instructor,
            "schedule": schedule,
            "room": room,
            "students": [],
            "assignments": []
        }

        self.data['classes'].append(new_class)
        self.save_data()
        print(f"Class '{name}' added successfully.")
        return True

    def add_student(self, class_id, student_id, name, email):
        """Add a student to a class"""
        cls = self.get_class(class_id)
        if not cls:
            print(f"Class '{class_id}' not found.")
            return False

        # Check if student already exists
        for student in cls['students']:
            if student['id'] == student_id:
                print(f"Student '{student_id}' already enrolled in this class.")
                return False

        new_student = {
            "id": student_id,
            "name": name,
            "email": email
        }

        cls['students'].append(new_student)
        self.save_data()
        print(f"Student '{name}' added to class '{cls['name']}'.")
        return True

    def add_assignment(self, class_id, assignment_id, title, due_date, max_points):
        """Add an assignment to a class"""
        cls = self.get_class(class_id)
        if not cls:
            print(f"Class '{class_id}' not found.")
            return False

        # Check if assignment already exists
        for assignment in cls['assignments']:
            if assignment['id'] == assignment_id:
                print(f"Assignment '{assignment_id}' already exists in this class.")
                return False

        new_assignment = {
            "id": assignment_id,
            "title": title,
            "due_date": due_date,
            "max_points": int(max_points),
            "grades": {}
        }

        cls['assignments'].append(new_assignment)
        self.save_data()
        print(f"Assignment '{title}' added to class '{cls['name']}'.")
        return True

    def record_grade(self, class_id, assignment_id, student_id, grade):
        """Record a grade for a student on an assignment"""
        cls = self.get_class(class_id)
        if not cls:
            print(f"Class '{class_id}' not found.")
            return False

        # Find assignment
        assignment = None
        for assgn in cls['assignments']:
            if assgn['id'] == assignment_id:
                assignment = assgn
                break

        if not assignment:
            print(f"Assignment '{assignment_id}' not found in class '{class_id}'.")
            return False

        # Check if student exists in class
        student_exists = any(s['id'] == student_id for s in cls['students'])
        if not student_exists:
            print(f"Student '{student_id}' not enrolled in class '{class_id}'.")
            return False

        grade_value = float(grade)
        if grade_value < 0 or grade_value > assignment['max_points']:
            print(f"Grade must be between 0 and {assignment['max_points']}.")
            return False

        assignment['grades'][student_id] = grade_value
        self.save_data()
        print(f"Grade {grade_value} recorded for student '{student_id}' on assignment '{assignment['title']}'.")
        return True

    def student_report(self, class_id, student_id):
        """Generate a report for a student in a class"""
        cls = self.get_class(class_id)
        if not cls:
            print(f"Class '{class_id}' not found.")
            return

        student = None
        for s in cls['students']:
            if s['id'] == student_id:
                student = s
                break

        if not student:
            print(f"Student '{student_id}' not enrolled in class '{class_id}'.")
            return

        print(f"\nStudent Report")
        print("=" * 60)
        print(f"Student: {student['name']} ({student['id']})")
        print(f"Class: {cls['name']} ({cls['id']})")
        print(f"Instructor: {cls['instructor']}")
        print()

        total_points = 0
        earned_points = 0

        print(f"{'Assignment':<30} {'Grade':<10} {'Max':<10} {'Status':<10}")
        print("-" * 60)

        for assignment in cls['assignments']:
            if student_id in assignment['grades']:
                grade = assignment['grades'][student_id]
                total_points += assignment['max_points']
                earned_points += grade
                percentage = (grade / assignment['max_points']) * 100
                print(f"{assignment['title']:<30} {grade:<10.1f} {assignment['max_points']:<10} {percentage:.1f}%")
            else:
                total_points += assignment['max_points']
                print(f"{assignment['title']:<30} {'Not Graded':<10} {assignment['max_points']:<10} {'Pending':<10}")

        print("-" * 60)
        if total_points > 0:
            overall_percentage = (earned_points / total_points) * 100
            print(f"Overall: {earned_points:.1f}/{total_points} ({overall_percentage:.1f}%)")
        print()

    def search(self, query):
        """Search for classes, students, or instructors"""
        query_lower = query.lower()
        results = []

        for cls in self.data['classes']:
            # Search in class name, ID, instructor
            if (query_lower in cls['name'].lower() or
                query_lower in cls['id'].lower() or
                query_lower in cls['instructor'].lower()):
                results.append(('class', cls))

            # Search in students
            for student in cls['students']:
                if (query_lower in student['name'].lower() or
                    query_lower in student['id'].lower() or
                    query_lower in student['email'].lower()):
                    results.append(('student', cls, student))

        if not results:
            print(f"No results found for '{query}'.")
            return

        print(f"\nSearch results for '{query}':")
        print("=" * 80)

        for result in results:
            if result[0] == 'class':
                cls = result[1]
                print(f"CLASS: {cls['name']} ({cls['id']}) - {cls['instructor']}")
            elif result[0] == 'student':
                cls, student = result[1], result[2]
                print(f"STUDENT: {student['name']} ({student['id']}) in {cls['name']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Class Management System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cms.py list                                    # List all classes
  cms.py view CS101                              # View class details
  cms.py add-class PHYS101 "Physics I" "Dr. Lee" "MWF 9:00" "Lab 201"
  cms.py add-student CS101 S004 "David Green" "david@example.com"
  cms.py add-assignment CS101 A003 "Final Project" "2025-12-15" 200
  cms.py grade CS101 A001 S001 95                # Record grade
  cms.py report CS101 S001                       # Student report
  cms.py search Alice                            # Search for anything
        """
    )

    parser.add_argument('action', choices=[
        'list', 'view', 'add-class', 'add-student',
        'add-assignment', 'grade', 'report', 'search'
    ])
    parser.add_argument('args', nargs='*', help='Arguments for the action')
    parser.add_argument('--data', default=Path(__file__).with_name('classes.json'))

    args = parser.parse_args()

    cms = ClassCMS(args.data)

    if args.action == 'list':
        cms.list_classes()

    elif args.action == 'view':
        if len(args.args) < 1:
            parser.error('view requires a class ID')
        cms.view_class(args.args[0])

    elif args.action == 'add-class':
        if len(args.args) < 5:
            parser.error('add-class requires: class_id name instructor schedule room')
        cms.add_class(args.args[0], args.args[1], args.args[2], args.args[3], args.args[4])

    elif args.action == 'add-student':
        if len(args.args) < 4:
            parser.error('add-student requires: class_id student_id name email')
        cms.add_student(args.args[0], args.args[1], args.args[2], args.args[3])

    elif args.action == 'add-assignment':
        if len(args.args) < 5:
            parser.error('add-assignment requires: class_id assignment_id title due_date max_points')
        cms.add_assignment(args.args[0], args.args[1], args.args[2], args.args[3], args.args[4])

    elif args.action == 'grade':
        if len(args.args) < 4:
            parser.error('grade requires: class_id assignment_id student_id grade')
        cms.record_grade(args.args[0], args.args[1], args.args[2], args.args[3])

    elif args.action == 'report':
        if len(args.args) < 2:
            parser.error('report requires: class_id student_id')
        cms.student_report(args.args[0], args.args[1])

    elif args.action == 'search':
        if len(args.args) < 1:
            parser.error('search requires a query string')
        cms.search(args.args[0])


if __name__ == '__main__':
    main()
