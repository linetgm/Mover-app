from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User

bp = Blueprint('admin', _name_)

@bp.route('/approve_mover/<int:mover_id>', methods=['POST'])
@jwt_required()
def approve_mover(mover_id):
    admin_id = get_jwt_identity()
    admin_user = User.query.get_or_404(admin_id)
    
    if admin_user.role != 'Admin':
        return jsonify({"msg": "Unauthorized"}), 403
    
    mover = User.query.get_or_404(mover_id)
    mover.approved = True
    db.session.commit()
    
    return jsonify({"msg": "Mover approved"}), 200

@bp.route('/reject_mover/<int:mover_id>', methods=['POST'])
@jwt_required()
def reject_mover(mover_id):
    admin_id = get_jwt_identity()
    admin_user = User.query.get_or_404(admin_id)
    
    if admin_user.role != 'Admin':
        return jsonify({"msg": "Unauthorized"}), 403
    
    mover = User.query.get_or_404(mover_id)
    mover.approved = False
    db.session.commit()
    
    return jsonify({"msg": "Mover rejected"}), 200

@bp.route('/delete_mover/<int:mover_id>', methods=['DELETE'])
@jwt_required()
def delete_mover(mover_id):
    admin_id = get_jwt_identity()
    admin_user = User.query.get_or_404(admin_id)
    
    if admin_user.role != 'Admin':
        return jsonify({"msg": "Unauthorized"}), 403
    
    mover = User.query.get_or_404(mover_id)
    db.session.delete(mover)
    db.session.commit()
    
    return jsonify({"msg": "Mover deleted"}), 200

@bp.route('/customers', methods=['GET'])
@jwt_required()
def list_customers():
    admin_id = get_jwt_identity()
    admin_user = User.query.get_or_404(admin_id)
    
    if admin_user.role != 'Admin':
        return jsonify({"msg": "Unauthorized"}), 403
    
    customers = User.query.filter_by(role='Customer').all()
    customer_list = [{
        "id": customer.id,
        "email": customer.email,
        "approved": customer.approved
    } for customer in customers]
    
    return jsonify(customer_list), 200

@bp.route('/movers', methods=['GET'])
@jwt_required()
def list_movers():
    admin_id = get_jwt_identity()
    admin_user = User.query.get_or_404(admin_id)
    
    if admin_user.role != 'Admin':
        return jsonify({"msg": "Unauthorized"}), 403
    
    movers = User.query.filter_by(role='Mover').all()
    mover_list = [{
        "id": mover.id,
        "email": mover.email,
        "approved": mover.approved
    } for mover in movers]
    
    return jsonify(mover_list), 200