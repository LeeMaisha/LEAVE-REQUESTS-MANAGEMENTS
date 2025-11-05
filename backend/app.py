from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leave_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    leave_requests = db.relationship('LeaveRequest', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'reason': self.reason,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# Auth Routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    hashed_password = generate_password_hash(data['password'])
    role = data.get('role', 'employee')
    
    # Only allow admin role if explicitly set (for demo purposes)
    if role not in ['admin', 'employee']:
        role = 'employee'
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=role
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': new_user.to_dict()
    }), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role}
    )
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

# Leave Request Routes
@app.route('/leaves', methods=['POST'])
@jwt_required()
def create_leave_request():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validation
    if not data.get('start_date') or not data.get('end_date') or not data.get('reason'):
        return jsonify({'error': 'Start date, end date, and reason are required'}), 400
    
    if not data['reason'].strip():
        return jsonify({'error': 'Reason cannot be empty'}), 400
    
    try:
        start_date = datetime.fromisoformat(data['start_date']).date()
        end_date = datetime.fromisoformat(data['end_date']).date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    if end_date < start_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    # Create leave request
    leave_request = LeaveRequest(
        user_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
        reason=data['reason'].strip(),
        status='pending'
    )
    
    db.session.add(leave_request)
    db.session.commit()
    
    return jsonify({
        'message': 'Leave request created successfully',
        'leave_request': leave_request.to_dict()
    }), 201

@app.route('/leaves', methods=['GET'])
@jwt_required()
def get_leave_requests():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role == 'admin':
        # Admin can see all requests
        leave_requests = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
    else:
        # Employee can only see their own requests
        leave_requests = LeaveRequest.query.filter_by(user_id=current_user_id).order_by(LeaveRequest.created_at.desc()).all()
    
    return jsonify({
        'leave_requests': [lr.to_dict() for lr in leave_requests]
    }), 200

@app.route('/leaves/<int:leave_id>/status', methods=['PATCH'])
@jwt_required()
def update_leave_status(leave_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # Only admins can update status
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized. Only admins can update leave status'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['approved', 'rejected']:
        return jsonify({'error': 'Status must be either approved or rejected'}), 400
    
    leave_request = LeaveRequest.query.get(leave_id)
    
    if not leave_request:
        return jsonify({'error': 'Leave request not found'}), 404
    
    leave_request.status = new_status
    db.session.commit()
    
    return jsonify({
        'message': f'Leave request {new_status} successfully',
        'leave_request': leave_request.to_dict()
    }), 200

# Initialize database and create admin user
@app.before_request
def create_tables():
    db.create_all()
    
    # Create default admin if not exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            name='Admin User',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin@example.com / admin123")
    
    app.run(debug=True, port=5000)