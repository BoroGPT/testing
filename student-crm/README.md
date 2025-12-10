# Student CRM

A modern, full-featured Customer Relationship Management (CRM) system designed specifically for managing student information. Built with Node.js, Express, SQLite, and vanilla JavaScript.

## Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete student records
- **Advanced Search**: Search students by name, email, or program
- **Filter by Status**: Quick filtering by enrollment status (Active, Graduated, On Leave, Withdrawn)
- **Comprehensive Student Data**:
  - Personal information (name, email, phone)
  - Academic details (program, GPA, enrollment dates)
  - Enrollment status tracking
  - Notes and additional information
- **Modern UI**: Clean, responsive interface with a purple gradient theme
- **Real-time Updates**: Instant reflection of changes without page reload
- **Data Validation**: Email uniqueness and required field validation
- **SQLite Database**: Lightweight, file-based database with no external dependencies

## Technology Stack

- **Backend**: Node.js with Express.js
- **Database**: SQLite with better-sqlite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: RESTful API design

## Installation

1. Navigate to the student-crm directory:
```bash
cd student-crm
```

2. Install dependencies:
```bash
npm install
```

3. Start the server:
```bash
npm start
```

4. Open your browser and navigate to:
```
http://localhost:3000
```

## Usage

### Adding a Student

1. Click the "Add New Student" button
2. Fill in the required fields (First Name, Last Name, Email)
3. Optionally add phone, program, enrollment dates, GPA, and notes
4. Click "Save Student"

### Editing a Student

1. Click the "Edit" button on any student card
2. Modify the information as needed
3. Click "Save Student"

### Deleting a Student

1. Click the "Delete" button on any student card
2. Confirm the deletion in the popup dialog

### Searching Students

1. Enter search terms in the search bar (searches name, email, and program)
2. Click "Search" or press Enter
3. Click "Clear" to reset the search

### Filtering by Status

Use the dropdown menu to filter students by their enrollment status:
- Active
- Graduated
- On Leave
- Withdrawn

## API Endpoints

### Get All Students
```
GET /api/students
Query Parameters:
  - search: Search term
  - status: Filter by enrollment status
```

### Get Single Student
```
GET /api/students/:id
```

### Create Student
```
POST /api/students
Body: JSON with student data
```

### Update Student
```
PUT /api/students/:id
Body: JSON with updated student data
```

### Delete Student
```
DELETE /api/students/:id
```

## Database Schema

The students table includes the following fields:
- `id`: Unique identifier (auto-increment)
- `first_name`: Student's first name (required)
- `last_name`: Student's last name (required)
- `email`: Student's email address (required, unique)
- `phone`: Contact phone number
- `program`: Academic program or major
- `enrollment_status`: Current status (active, graduated, on_leave, withdrawn)
- `enrollment_date`: Date of enrollment
- `graduation_date`: Expected or actual graduation date
- `gpa`: Grade point average
- `notes`: Additional notes or information
- `created_at`: Timestamp of record creation
- `updated_at`: Timestamp of last update

## Development

To run in development mode:
```bash
npm run dev
```

The server will start on port 3000 by default. You can change this by setting the PORT environment variable:
```bash
PORT=8080 npm start
```

## Project Structure

```
student-crm/
├── src/
│   ├── database.js    # Database setup and queries
│   └── server.js      # Express server and API routes
├── public/
│   ├── index.html     # Main HTML page
│   ├── styles.css     # CSS styling
│   └── app.js         # Frontend JavaScript
├── package.json       # Dependencies and scripts
├── students.db        # SQLite database (created on first run)
└── README.md          # This file
```

## Security Features

- Input validation on both frontend and backend
- SQL injection prevention using prepared statements
- XSS prevention with HTML escaping
- Email uniqueness constraints
- Proper error handling

## Browser Support

Works on all modern browsers including:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
