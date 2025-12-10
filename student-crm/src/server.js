const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const {
  getAllStudents,
  getStudentById,
  searchStudents,
  filterByStatus,
  createStudent,
  updateStudent,
  deleteStudent
} = require('./database');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '..', 'public')));

app.get('/api/students', (req, res) => {
  try {
    const { search, status } = req.query;

    let students;
    if (search) {
      const searchTerm = `%${search}%`;
      students = searchStudents.all(searchTerm, searchTerm, searchTerm, searchTerm);
    } else if (status) {
      students = filterByStatus.all(status);
    } else {
      students = getAllStudents.all();
    }

    res.json(students);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/students/:id', (req, res) => {
  try {
    const student = getStudentById.get(req.params.id);
    if (student) {
      res.json(student);
    } else {
      res.status(404).json({ error: 'Student not found' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/api/students', (req, res) => {
  try {
    const {
      first_name,
      last_name,
      email,
      phone,
      program,
      enrollment_status,
      enrollment_date,
      graduation_date,
      gpa,
      notes
    } = req.body;

    if (!first_name || !last_name || !email) {
      return res.status(400).json({ error: 'First name, last name, and email are required' });
    }

    const result = createStudent.run(
      first_name,
      last_name,
      email,
      phone || null,
      program || null,
      enrollment_status || 'active',
      enrollment_date || null,
      graduation_date || null,
      gpa || null,
      notes || null
    );

    const newStudent = getStudentById.get(result.lastInsertRowid);
    res.status(201).json(newStudent);
  } catch (error) {
    if (error.message.includes('UNIQUE constraint failed')) {
      res.status(400).json({ error: 'Email already exists' });
    } else {
      res.status(500).json({ error: error.message });
    }
  }
});

app.put('/api/students/:id', (req, res) => {
  try {
    const {
      first_name,
      last_name,
      email,
      phone,
      program,
      enrollment_status,
      enrollment_date,
      graduation_date,
      gpa,
      notes
    } = req.body;

    if (!first_name || !last_name || !email) {
      return res.status(400).json({ error: 'First name, last name, and email are required' });
    }

    const result = updateStudent.run(
      first_name,
      last_name,
      email,
      phone || null,
      program || null,
      enrollment_status || 'active',
      enrollment_date || null,
      graduation_date || null,
      gpa || null,
      notes || null,
      req.params.id
    );

    if (result.changes === 0) {
      return res.status(404).json({ error: 'Student not found' });
    }

    const updatedStudent = getStudentById.get(req.params.id);
    res.json(updatedStudent);
  } catch (error) {
    if (error.message.includes('UNIQUE constraint failed')) {
      res.status(400).json({ error: 'Email already exists' });
    } else {
      res.status(500).json({ error: error.message });
    }
  }
});

app.delete('/api/students/:id', (req, res) => {
  try {
    const result = deleteStudent.run(req.params.id);
    if (result.changes === 0) {
      return res.status(404).json({ error: 'Student not found' });
    }
    res.json({ message: 'Student deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Student CRM server running on http://localhost:${PORT}`);
});
