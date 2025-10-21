# Class Management System (CMS)

This repository contains a comprehensive Class Management System for managing courses, students, assignments, and grades.

## Features

- Manage multiple classes with instructor and schedule information
- Track students enrolled in each class
- Create and manage assignments with due dates
- Record and track grades for students
- Generate student progress reports
- Search functionality across classes and students

## Installation

Requires Python 3.6 or higher. No external dependencies needed.

## Usage

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

---

## Magic the Gathering Codex

This repository also contains a small example codex for Magic the Gathering cards.

### Usage

```bash
python codex/codex.py list
python codex/codex.py search Lotus
```

The card data lives in `codex/cards.json`.
