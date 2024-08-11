from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User, Inventory, Move, Mover, Message
from datetime import datetime

bp = Blueprint('routes', _name_)

@bp.route('/home_types', methods=['GET'])
def get_home_types():
    home_types = [
        {'id': 1, 'type': 'Bedsitter'},
        {'id': 2, 'type': 'One Bedroom'},
        {'id': 3, 'type': 'Studio'},
        {'id': 4, 'type': 'Two Bedroom'},
    ]
    return jsonify(home_types)

@bp.route('/inventory', methods=['POST'])
@jwt_required()
def create_inventory():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    inventory = Inventory(user_id=user_id, house_type=data['house_type'], items=data['items'])
    db.session.add(inventory)
    db.session.commit()
    
    return jsonify({"msg": "Inventory created"}), 201

@bp.route('/move', methods=['POST'])
@jwt_required()
def book_move():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    move = Move(
        user_id=user_id,
        current_location=data['current_location'],
        new_location=data['new_location'],
        moving_date=datetime.strptime(data['moving_date'], '%Y-%m-%d')
    )
    db.session.add(move)
    db.session.commit()
    
    return jsonify({"msg": "Move booked"}), 201

@bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    user_id = get_jwt_identity()
    inventory = Inventory.query.filter_by(user_id=user_id).all()

    if not inventory:
        return jsonify({"msg": "No inventory found"}), 404

    inventory_list = [{
        "id": item.id,
        "house_type": item.house_type,
        "items": item.items
    } for item in inventory]

    return jsonify(inventory_list), 200



@bp.route('/move/<int:move_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_move(move_id):
    mover_id = get_jwt_identity()
    move = Move.query.get_or_404(move_id)
    
    if move.mover_id is not None:
        return jsonify({"msg": "Move already confirmed"}), 400
    
    move.mover_id = mover_id
    move.status = "Confirmed"
    db.session.commit()
    
    # Notification logic here (e.g., send email to customer)
    
    return jsonify({"msg": "Move confirmed"}), 200

@bp.route('/mover/bookings', methods=['GET'])
@jwt_required()
def view_mover_bookings():
    mover_id = get_jwt_identity()
    moves = Move.query.filter_by(mover_id=mover_id).all()
    
    bookings = [{
        "id": move.id,
        "current_location": move.current_location,
        "new_location": move.new_location,
        "moving_date": move.moving_date,
        "status": move.status
    } for move in moves]
    
    return jsonify(bookings), 200

@bp.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    message = Message(
        sender_id=user_id,
        receiver_id=data['receiver_id'],
        move_id=data['move_id'],
        content=data['content']
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({"msg": "Message sent"}), 201

@bp.route('/get_messages/<int:move_id>', methods=['GET'])
@jwt_required()
def get_messages(move_id):
    user_id = get_jwt_identity()
    move = Move.query.filter_by(id=move_id).first()

    if not move or (move.user_id != user_id and move.mover_id != user_id):
        return jsonify({"msg": "Unauthorized or move not found"}), 403

    messages = Message.query.filter_by(move_id=move_id).order_by(Message.timestamp.asc()).all()

    message_list = [{
        "sender_id": message.sender_id,
        "content": message.content,
        "timestamp": message.timestamp
    } for message in messages]

    return jsonify(message_list), 200