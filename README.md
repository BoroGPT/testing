# Class Management System (CMS)

This repository contains a comprehensive Class Management System for managing courses, students, assignments, and grades.

## Features

- Modern web interface with beautiful, responsive design
- Manage multiple classes with instructor and schedule information
- Track students enrolled in each class
- Create and manage assignments with due dates
- Record and track grades for students
- Generate detailed student progress reports with print support
- Search functionality across classes and students
- Real-time form validation
- Mobile-friendly responsive layout

## Quick Start - Web Application

### Installation

1. Install Python 3.6 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the Web App

```bash
cd cms
python app.py
```

Then open your browser to: **http://localhost:5000**

The web interface provides:
- Dashboard with all classes
- Class detail pages with students and assignments
- Grade management interface
- Student progress reports
- Search functionality
- Easy forms for adding/editing data

## Command Line Usage

### List All Classes

```bash
python cms/cms.py list
```

### View Class Details

```bash
python cms/cms.py view CS101
```

### Add a New Class

```bash
python cms/cms.py add-class PHYS101 "Physics I" "Dr. Lee" "MWF 9:00" "Lab 201"
```

### Add a Student to a Class

```bash
python cms/cms.py add-student CS101 S004 "David Green" "david@example.com"
```

### Add an Assignment to a Class

```bash
python cms/cms.py add-assignment CS101 A003 "Final Project" "2025-12-15" 200
```

### Record a Grade

```bash
python cms/cms.py grade CS101 A001 S001 95
```

### Generate Student Report

```bash
python cms/cms.py report CS101 S001
```

### Search

```bash
python cms/cms.py search Alice
```

## Data Storage

All class data is stored in `cms/classes.json`. The file includes:
- Class information (ID, name, instructor, schedule, room)
- Student roster with contact information
- Assignments with due dates and maximum points
- Grades for each student on each assignment

You can manually edit this file or use the CMS commands to manage your data.

## Example Workflow

```bash
# Create a new class
python cms/cms.py add-class ENG201 "English Literature" "Prof. Martinez" "TTh 13:00" "Hall 301"

# Enroll students
python cms/cms.py add-student ENG201 S005 "Emma Watson" "emma@example.com"
python cms/cms.py add-student ENG201 S006 "Liam Chen" "liam@example.com"

# Create an assignment
python cms/cms.py add-assignment ENG201 A001 "Essay: Shakespeare Analysis" "2025-11-20" 100

# Record grades
python cms/cms.py grade ENG201 A001 S005 92
python cms/cms.py grade ENG201 A001 S006 88

# View student progress
python cms/cms.py report ENG201 S005
```

## Deploying to Production

### Deploy to Render (Free)

1. Create a free account at [Render.com](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd cms && python app.py`
   - **Environment**: Python 3
5. Click "Create Web Service"

Your CMS will be live at a free `.onrender.com` URL!

### Deploy to Railway (Free)

1. Create account at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and uses `requirements.txt`
5. Set start command: `cd cms && python app.py`

### Deploy to Heroku

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a `Procfile` in the root directory:
   ```
   web: cd cms && gunicorn app:app
   ```
3. Add `gunicorn` to `requirements.txt`
4. Deploy:
   ```bash
   heroku create your-cms-app
   git push heroku main
   ```

### Environment Configuration

For production, update the secret key in `cms/app.py`:
```python
app.secret_key = 'your-secure-random-secret-key-here'
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Project Structure

```
.
├── cms/
│   ├── app.py              # Flask web application
│   ├── cms.py              # Command-line interface
│   ├── classes.json        # Data storage
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── class_detail.html
│   │   ├── add_class.html
│   │   ├── edit_class.html
│   │   ├── add_student.html
│   │   ├── add_assignment.html
│   │   ├── manage_grades.html
│   │   ├── student_report.html
│   │   └── search_results.html
│   └── static/
│       ├── css/
│       │   └── style.css   # Modern, responsive styles
│       └── js/
│           └── main.js     # Interactive features
├── codex/                  # MTG card codex
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Magic the Gathering Codex

This repository also contains a small example codex for Magic the Gathering cards.

### Usage

```bash
python codex/codex.py list
python codex/codex.py search Lotus
```

The card data lives in `codex/cards.json`.
