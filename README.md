# LEAVE-REQUESTS-MANAGEMENTS
LEAVE-REQUESTS-MANAGEMENTS
Leave Request Management System
Project Overview
A full-stack web application for managing employee leave requests with role-based access control. Employees can submit leave requests and view their status, while admins can approve or reject requests and view system statistics.

Technology Stack
Backend
Framework: Flask
Database: SQLite with SQLAlchemy ORM
Authentication: JWT (JSON Web Tokens)
CORS: Flask-CORS for cross-origin requests
Frontend
Framework: React
Routing: React Router DOM
HTTP Client: Axios
State Management: React Context API
Project Structure
LEAVE-REQUESTS-MANAGEMENTS/
├── leave-management-backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── config.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── leaves.py
│   │       └── admin.py
│   ├── seed.py
│   ├── run.py
│   ├── requirements.txt
│   └── leave_management.db
└── leave-management-frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── Login.js
    │   │   ├── EmployeeDashboard.js
    │   │   └── AdminDashboard.js
    │   ├── context/
    │   │   └── AuthContext.js
    │   ├── App.js
    │   ├── index.js
    │   └── index.css
    ├── package.json
    └── package-lock.json
Features
User Roles
Admin
View all leave requests
Approve or reject leave requests
View employee list
View system statistics (total requests, pending, approved, rejected)
Access admin dashboard
Employee
Submit new leave requests
View personal leave request history
See request status (pending, approved, rejected)
Access employee dashboard
Authentication & Authorization
JWT-based authentication
Role-based route protection
Persistent login sessions
Secure password hashing
Installation & Setup
Prerequisites
Python 3.8+
Node.js 14+
npm or yarn
Backend Setup
Navigate to backend directory:
cd leave-management-backend
Create virtual environment and activate:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Initialize database:
python seed.py
Start the backend server:
python run.py
The backend will run on http://localhost:5000

Frontend Setup
Navigate to frontend directory:
cd leave-management-frontend
Install dependencies:
npm install
Start the development server:
npm start
The frontend will run on http://localhost:3000

API Endpoints
Authentication
POST /auth/register - Register new user
POST /auth/login - Authenticate user and get JWT token
Leave Requests
POST /leaves - Create new leave request (Employee only)
GET /leaves - Get leave requests (All users, filtered by role)
Admin Operations
PATCH /leaves/<id>/status - Update leave request status (Admin only)
GET /users - Get all users (Admin only)
GET /stats - Get system statistics (Admin only)
Default Users
The system comes with pre-seeded users:

Admin User:

Email: admin@company.com
Password: admin123
Employee Users:

Email: john@company.com
Password: password123
Email: jane@company.com
Password: password123
Usage
Access the application at http://localhost:3000
Login with provided credentials
Employees can submit leave requests and view their history
Admins can manage all leave requests and view system statistics
Register new users if needed
Deployment Notes
Backend Deployment
Use production WSGI server (Gunicorn)
Set proper JWT secret key in production
Use PostgreSQL or MySQL in production
Configure CORS for production domain
Frontend Deployment
Build for production: npm run build
Serve with Nginx or Apache
Update API URLs for production environment
Development
Backend Development
Flask debug mode enabled
SQLite database for development
Automatic database creation on first run
Frontend Development
Hot reload enabled
Development server with error overlay
React DevTools recommended
Testing
Test the backend API:

cd leave-management-backend
python test_backend.py
Security Features
Password hashing with Werkzeug
JWT token expiration
Role-based access control
Input validation
SQL injection prevention with ORM
CORS configuration
Error Handling
Comprehensive error responses
User-friendly error messages
Server-side validation
Client-side error handling
Browser Support
Modern browsers (Chrome, Firefox, Safari, Edge)
Mobile responsive design
Progressive Web App ready
License
This project is for educational and internal business use.

Support
For issues and questions, please check the API documentation or contact the development team.
