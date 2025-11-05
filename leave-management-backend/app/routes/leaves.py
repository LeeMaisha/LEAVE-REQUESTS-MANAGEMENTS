from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import LeaveRequest, User
from datetime import datetime

leaves_bp = Blueprint('leaves', __name__)

@leaves_bp.route('/leaves', methods=['POST'])
@jwt_required()
def create_leave_request():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or not all(key in data for key in ['start_date', 'end_date', 'reason']):
            return jsonify({'error': 'Start date, end date and reason are required'}), 400
        
        if not data['start_date'] or not data['end_date'] or not data['reason']:
            return jsonify({'error': 'All fields are required'}), 400
        
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
            
            if start_date > end_date:
                return jsonify({'error': 'Start date cannot be after end date'}), 400
                
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        leave_request = LeaveRequest(
            user_id=current_user['id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            reason=data['reason']
        )
        
        db.session.add(leave_request)
        db.session.commit()
        
        return jsonify({'message': 'Leave request submitted successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leaves_bp.route('/leaves', methods=['GET'])
@jwt_required()
def get_leave_requests():
    try:
        current_user = get_jwt_identity()
        
        if current_user['role'] == 'admin':
            leave_requests = LeaveRequest.query.join(User).order_by(LeaveRequest.created_at.desc()).all()
            result = [leave.to_dict() for leave in leave_requests]
        else:
            leave_requests = LeaveRequest.query.filter_by(user_id=current_user['id']).order_by(LeaveRequest.created_at.desc()).all()
            result = [{
                'id': leave.id,
                'start_date': leave.start_date,
                'end_date': leave.end_date,
                'reason': leave.reason,
                'status': leave.status,
                'created_at': leave.created_at.isoformat()
            } for leave in leave_requests]
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500