const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, '..', 'students.db');
const db = new Database(dbPath);

db.exec(`
  CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    program TEXT,
    enrollment_status TEXT DEFAULT 'active',
    enrollment_date TEXT,
    graduation_date TEXT,
    gpa REAL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`);

db.exec(`
  CREATE INDEX IF NOT EXISTS idx_email ON students(email);
  CREATE INDEX IF NOT EXISTS idx_status ON students(enrollment_status);
  CREATE INDEX IF NOT EXISTS idx_name ON students(last_name, first_name);
`);

const getAllStudents = db.prepare('SELECT * FROM students ORDER BY last_name, first_name');

const getStudentById = db.prepare('SELECT * FROM students WHERE id = ?');

const searchStudents = db.prepare(`
  SELECT * FROM students
  WHERE first_name LIKE ?
     OR last_name LIKE ?
     OR email LIKE ?
     OR program LIKE ?
  ORDER BY last_name, first_name
`);

const filterByStatus = db.prepare(`
  SELECT * FROM students
  WHERE enrollment_status = ?
  ORDER BY last_name, first_name
`);

const createStudent = db.prepare(`
  INSERT INTO students (
    first_name, last_name, email, phone, program,
    enrollment_status, enrollment_date, graduation_date, gpa, notes
  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const updateStudent = db.prepare(`
  UPDATE students
  SET first_name = ?,
      last_name = ?,
      email = ?,
      phone = ?,
      program = ?,
      enrollment_status = ?,
      enrollment_date = ?,
      graduation_date = ?,
      gpa = ?,
      notes = ?,
      updated_at = CURRENT_TIMESTAMP
  WHERE id = ?
`);

const deleteStudent = db.prepare('DELETE FROM students WHERE id = ?');

module.exports = {
  db,
  getAllStudents,
  getStudentById,
  searchStudents,
  filterByStatus,
  createStudent,
  updateStudent,
  deleteStudent
};
