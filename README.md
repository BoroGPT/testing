# Student CRM

This repository contains a lightweight command-line CRM for tracking student
relationships throughout your recruitment pipeline. You can record contact
information, stages, owners, tags, and time-stamped notes for each student. The
student records live in `crm/students.json`.

## Installation

The tool only requires Python 3.8 or newer. Clone the repository and run the
commands below from the project root.

```bash
python crm/crm.py --help
```

## Usage

The CLI is organised into subcommands. The most common workflows are:

### List students

```bash
python crm/crm.py list
```

Filter the list by stage, status, owner, or tag:

```bash
python crm/crm.py list --status Prospect --owner "Priya Shah"
```

### Search the CRM

Search across all fields or focus on one in particular:

```bash
python crm/crm.py search Lopez
python crm/crm.py search scholarship --field notes
```

### View details for a single student

```bash
python crm/crm.py info stu-002
```

### Add and update students

```bash
python crm/crm.py add "Elena" "Fischer" elena.fischer@example.edu --status Applicant --stage Interview --owner "Jordan Rivera" --tag STEM --tag Honors
python crm/crm.py update stu-004 --stage "Application Review" --tag Engineering --tag Robotics
```

### Capture notes

```bash
python crm/crm.py add-note stu-001 "Emailed financial aid packet" --author "Jordan Rivera"
```

All mutating commands update the JSON data file in-place. Provide a custom file
with `--data` if you want to work with a different dataset.
