let currentEditId = null;

async function loadStudents(queryParams = '') {
    try {
        const response = await fetch(`/api/students${queryParams}`);
        const students = await response.json();
        displayStudents(students);
    } catch (error) {
        console.error('Error loading students:', error);
        alert('Failed to load students');
    }
}

function displayStudents(students) {
    const container = document.getElementById('studentsContainer');
    const countElement = document.getElementById('studentCount');

    countElement.textContent = students.length;

    if (students.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No students found</h3>
                <p>Add your first student to get started!</p>
            </div>
        `;
        return;
    }

    container.innerHTML = students.map(student => `
        <div class="student-card">
            <div class="student-header">
                <div class="student-name">${escapeHtml(student.first_name)} ${escapeHtml(student.last_name)}</div>
                <span class="student-status status-${student.enrollment_status}">${formatStatus(student.enrollment_status)}</span>
            </div>
            <div class="student-details">
                <div class="detail-item">
                    <span class="detail-label">Email</span>
                    <span>${escapeHtml(student.email)}</span>
                </div>
                ${student.phone ? `
                <div class="detail-item">
                    <span class="detail-label">Phone</span>
                    <span>${escapeHtml(student.phone)}</span>
                </div>
                ` : ''}
                ${student.program ? `
                <div class="detail-item">
                    <span class="detail-label">Program</span>
                    <span>${escapeHtml(student.program)}</span>
                </div>
                ` : ''}
                ${student.enrollment_date ? `
                <div class="detail-item">
                    <span class="detail-label">Enrollment Date</span>
                    <span>${formatDate(student.enrollment_date)}</span>
                </div>
                ` : ''}
                ${student.graduation_date ? `
                <div class="detail-item">
                    <span class="detail-label">Graduation Date</span>
                    <span>${formatDate(student.graduation_date)}</span>
                </div>
                ` : ''}
                ${student.gpa ? `
                <div class="detail-item">
                    <span class="detail-label">GPA</span>
                    <span>${student.gpa.toFixed(2)}</span>
                </div>
                ` : ''}
            </div>
            ${student.notes ? `
            <div class="student-notes">
                <strong>Notes:</strong><br>
                ${escapeHtml(student.notes)}
            </div>
            ` : ''}
            <div class="student-actions">
                <button class="btn-edit" onclick="editStudent(${student.id})">Edit</button>
                <button class="btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function showAddStudentForm() {
    currentEditId = null;
    document.getElementById('formTitle').textContent = 'Add New Student';
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    document.getElementById('studentFormModal').style.display = 'block';
}

async function editStudent(id) {
    try {
        const response = await fetch(`/api/students/${id}`);
        const student = await response.json();

        currentEditId = id;
        document.getElementById('formTitle').textContent = 'Edit Student';
        document.getElementById('studentId').value = id;
        document.getElementById('firstName').value = student.first_name;
        document.getElementById('lastName').value = student.last_name;
        document.getElementById('email').value = student.email;
        document.getElementById('phone').value = student.phone || '';
        document.getElementById('program').value = student.program || '';
        document.getElementById('enrollmentStatus').value = student.enrollment_status;
        document.getElementById('enrollmentDate').value = student.enrollment_date || '';
        document.getElementById('graduationDate').value = student.graduation_date || '';
        document.getElementById('gpa').value = student.gpa || '';
        document.getElementById('notes').value = student.notes || '';

        document.getElementById('studentFormModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading student:', error);
        alert('Failed to load student details');
    }
}

async function submitStudent(event) {
    event.preventDefault();

    const studentData = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        program: document.getElementById('program').value,
        enrollment_status: document.getElementById('enrollmentStatus').value,
        enrollment_date: document.getElementById('enrollmentDate').value,
        graduation_date: document.getElementById('graduationDate').value,
        gpa: document.getElementById('gpa').value,
        notes: document.getElementById('notes').value
    };

    try {
        const url = currentEditId ? `/api/students/${currentEditId}` : '/api/students';
        const method = currentEditId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(studentData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save student');
        }

        closeModal();
        loadStudents();
    } catch (error) {
        console.error('Error saving student:', error);
        alert(error.message);
    }
}

async function deleteStudent(id) {
    if (!confirm('Are you sure you want to delete this student? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`/api/students/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete student');
        }

        loadStudents();
    } catch (error) {
        console.error('Error deleting student:', error);
        alert('Failed to delete student');
    }
}

function searchStudents() {
    const searchTerm = document.getElementById('searchInput').value;
    if (searchTerm.trim()) {
        loadStudents(`?search=${encodeURIComponent(searchTerm)}`);
    } else {
        loadStudents();
    }
}

function clearSearch() {
    document.getElementById('searchInput').value = '';
    document.getElementById('statusFilter').value = '';
    loadStudents();
}

function filterByStatus() {
    const status = document.getElementById('statusFilter').value;
    if (status) {
        loadStudents(`?status=${encodeURIComponent(status)}`);
    } else {
        loadStudents();
    }
}

function closeModal() {
    document.getElementById('studentFormModal').style.display = 'none';
    document.getElementById('studentForm').reset();
    currentEditId = null;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatStatus(status) {
    return status.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

window.onclick = function(event) {
    const modal = document.getElementById('studentFormModal');
    if (event.target === modal) {
        closeModal();
    }
}

document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        searchStudents();
    }
});

loadStudents();
