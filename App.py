from flask import Flask, request, session, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from config import db
from Models import User, Profile, Checklist, Inventory, Move, Quote, Booking, Notification, Communication, MovingCompany
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Authentication and User Management
class Signup(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.verify_password(data['password']):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        return {}, 204

# User Resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.username = data['username']
            user.email = data['email']
            if 'password' in data:
                user.password = data['password']
            db.session.commit()
            return user.to_dict(), 200
        return {'error': 'User not found'}, 404

# Profile Resource
class ProfileResource(Resource):
    def get(self, profile_id=None):
        if profile_id:
            profile = Profile.query.get(profile_id)
            if profile:
                return profile.to_dict(), 200
            return {'error': 'Profile not found'}, 404
        profiles = Profile.query.all()
        return [profile.to_dict() for profile in profiles], 200

    def post(self):
        data = request.get_json()
        new_profile = Profile(
            user_id=data['user_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            preferences=data['preferences']
        )
        db.session.add(new_profile)
        db.session.commit()
        return new_profile.to_dict(), 201

    def put(self, profile_id):
        data = request.get_json()
        profile = Profile.query.get(profile_id)
        if profile:
            profile.user_id = data['user_id']
            profile.first_name = data['first_name']
            profile.last_name = data['last_name']
            profile.phone_number = data['phone_number']
            profile.preferences = data['preferences']
            db.session.commit()
            return profile.to_dict(), 200
        return {'error': 'Profile not found'}, 404

    def delete(self, profile_id):
        profile = Profile.query.get(profile_id)
        if profile:
            db.session.delete(profile)
            db.session.commit()
            return {}, 204
        return {'error': 'Profile not found'}, 404

# Checklist Resource
class ChecklistResource(Resource):
    def get(self, checklist_id=None):
        if checklist_id:
            checklist = Checklist.query.get(checklist_id)
            if checklist:
                return checklist.to_dict(), 200
            return {'error': 'Checklist not found'}, 404
        checklists = Checklist.query.all()
        return [checklist.to_dict() for checklist in checklists], 200

    def post(self):
        data = request.get_json()
        new_checklist = Checklist(
            user_id=data['user_id'],
            home_type=data['home_type']
        )
        db.session.add(new_checklist)
        db.session.commit()
        return new_checklist.to_dict(), 201

    def put(self, checklist_id):
        data = request.get_json()
        checklist = Checklist.query.get(checklist_id)
        if checklist:
            checklist.user_id = data['user_id']
            checklist.home_type = data['home_type']
            db.session.commit()
            return checklist.to_dict(), 200
        return {'error': 'Checklist not found'}, 404

    def delete(self, checklist_id):
        checklist = Checklist.query.get(checklist_id)
        if checklist:
            db.session.delete(checklist)
            db.session.commit()
            return {}, 204
        return {'error': 'Checklist not found'}, 404

# Inventory Resource
class InventoryResource(Resource):
    def get(self, inventory_id=None):
        if inventory_id:
            inventory = Inventory.query.get(inventory_id)
            if inventory:
                return inventory.to_dict(), 200
            return {'error': 'Inventory not found'}, 404
        inventories = Inventory.query.all()
        return [inventory.to_dict() for inventory in inventories], 200

    def post(self):
        data = request.get_json()
        new_inventory = Inventory(
            checklist_id=data['checklist_id'],
            item_name=data['item_name'],
            status=data['status'],
            notes=data['notes']
        )
        db.session.add(new_inventory)
        db.session.commit()
        return new_inventory.to_dict(), 201

    def put(self, inventory_id):
        data = request.get_json()
        inventory = Inventory.query.get(inventory_id)
        if inventory:
            inventory.checklist_id = data['checklist_id']
            inventory.item_name = data['item_name']
            inventory.status = data['status']
            inventory.notes = data['notes']
            db.session.commit()
            return inventory.to_dict(), 200
        return {'error': 'Inventory not found'}, 404

    def delete(self, inventory_id):
        inventory = Inventory.query.get(inventory_id)
        if inventory:
            db.session.delete(inventory)
            db.session.commit()
            return {}, 204
        return {'error': 'Inventory not found'}, 404

# Move Resource
class MoveResource(Resource):
    def get(self, move_id=None):
        if move_id:
            move = Move.query.get(move_id)
            if move:
                return move.to_dict(), 200
            return {'error': 'Move not found'}, 404
        moves = Move.query.all()
        return [move.to_dict() for move in moves], 200

    def post(self):
        data = request.get_json()
        new_move = Move(
            user_id=data['user_id'],
            company_id=data['company_id'],
            current_address=data['current_address'],
            new_address=data['new_address'],
            moving_date=datetime.strptime(data['moving_date'], '%Y-%m-%d').date(),
            special_requirements=data['special_requirements']
        )
        db.session.add(new_move)
        db.session.commit()
        return new_move.to_dict(), 201

    def put(self, move_id):
        data = request.get_json()
        move = Move.query.get(move_id)
        if move:
            move.user_id = data['user_id']
            move.company_id = data['company_id']
            move.current_address = data['current_address']
            move.new_address = data['new_address']
            move.moving_date = datetime.strptime(data['moving_date'], '%Y-%m-%d').date()
            move.special_requirements = data['special_requirements']
            db.session.commit()
            return move.to_dict(), 200
        return {'error': 'Move not found'}, 404

    def delete(self, move_id):
        move = Move.query.get(move_id)
        if move:
            db.session.delete(move)
            db.session.commit()
            return {}, 204
        return {'error': 'Move not found'}, 404

# Quote Resource
class QuoteResource(Resource):
    def get(self, quote_id=None):
        if quote_id:
            quote = Quote.query.get(quote_id)
            if quote:
                return quote.to_dict(), 200
            return {'error': 'Quote not found'}, 404
        quotes = Quote.query.all()
        return [quote.to_dict() for quote in quotes], 200

    def post(self):
        data = request.get_json()
        new_quote = Quote(
            move_id=data['move_id'],
            price=data['price'],
            status=data['status']
        )
        db.session.add(new_quote)
        db.session.commit()
        return new_quote.to_dict(), 201

    def put(self, quote_id):
        data = request.get_json()
        quote = Quote.query.get(quote_id)
        if quote:
            quote.move_id = data['move_id']
            quote.price = data['price']
            quote.status = data['status']
            db.session.commit()
            return quote.to_dict(), 200
        return {'error': 'Quote not found'}, 404

    def delete(self, quote_id):
        quote = Quote.query.get(quote_id)
        if quote:
            db.session.delete(quote)
            db.session.commit()
            return {}, 204
        return {'error': 'Quote not found'}, 404

# Booking Resource
class BookingResource(Resource):
    def get(self, booking_id=None):
        if booking_id:
            booking = Booking.query.get(booking_id)
            if booking:
                return booking.to_dict(), 200
            return {'error': 'Booking not found'}, 404
        bookings = Booking.query.all()
        return [booking.to_dict() for booking in bookings], 200

    def post(self):
        data = request.get_json()
        new_booking = Booking(
            move_id=data['move_id'],
            status=data['status'],
            booked_date=datetime.strptime(data['booked_date'], '%Y-%m-%d').date()
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.to_dict(), 201

    def put(self, booking_id):
        data = request.get_json()
        booking = Booking.query.get(booking_id)
        if booking:
            booking.move_id = data['move_id']
            booking.status = data['status']
            booking.booked_date = datetime.strptime(data['booked_date'], '%Y-%m-%d').date()
            db.session.commit()
            return booking.to_dict(), 200
        return {'error': 'Booking not found'}, 404

    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {}, 204
        return {'error': 'Booking not found'}, 404

# Notification Resource
class NotificationResource(Resource):
    def get(self, notification_id=None):
        if notification_id:
            notification = Notification.query.get(notification_id)
            if notification:
                return notification.to_dict(), 200
            return {'error': 'Notification not found'}, 404
        notifications = Notification.query.all()
        return [notification.to_dict() for notification in notifications], 200

    def post(self):
        data = request.get_json()
        new_notification = Notification(
            user_id=data['user_id'],
            message=data['message'],
            status=data['status']
        )
        db.session.add(new_notification)
        db.session.commit()
        return new_notification.to_dict(), 201

    def put(self, notification_id):
        data = request.get_json()
        notification = Notification.query.get(notification_id)
        if notification:
            notification.user_id = data['user_id']
            notification.message = data['message']
            notification.status = data['status']
            db.session.commit()
            return notification.to_dict(), 200
        return {'error': 'Notification not found'}, 404

    def delete(self, notification_id):
        notification = Notification.query.get(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return {}, 204
        return {'error': 'Notification not found'}, 404

# Communication Resource
class CommunicationResource(Resource):
    def get(self, communication_id=None):
        if communication_id:
            communication = Communication.query.get(communication_id)
            if communication:
                return communication.to_dict(), 200
            return {'error': 'Communication not found'}, 404
        communications = Communication.query.all()
        return [communication.to_dict() for communication in communications], 200

    def post(self):
        data = request.get_json()
        new_communication = Communication(
            user_id=data['user_id'],
            content=data['content'],
            sent_at=datetime.strptime(data['sent_at'], '%Y-%m-%d %H:%M:%S')
        )
        db.session.add(new_communication)
        db.session.commit()
        return new_communication.to_dict(), 201

    def put(self, communication_id):
        data = request.get_json()
        communication = Communication.query.get(communication_id)
        if communication:
            communication.user_id = data['user_id']
            communication.content = data['content']
            communication.sent_at = datetime.strptime(data['sent_at'], '%Y-%m-%d %H:%M:%S')
            db.session.commit()
            return communication.to_dict(), 200
        return {'error': 'Communication not found'}, 404

    def delete(self, communication_id):
        communication = Communication.query.get(communication_id)
        if communication:
            db.session.delete(communication)
            db.session.commit()
            return {}, 204
        return {'error': 'Communication not found'}, 404

# Moving Company Resource
class MovingCompanyResource(Resource):
    def get(self, company_id=None):
        if company_id:
            company = MovingCompany.query.get(company_id)
            if company:
                return company.to_dict(), 200
            return {'error': 'Company not found'}, 404
        companies = MovingCompany.query.all()
        return [company.to_dict() for company in companies], 200

    def post(self):
        data = request.get_json()
        new_company = MovingCompany(
            name=data['name'],
            address=data['address'],
            phone_number=data['phone_number'],
            email=data['email']
        )
        db.session.add(new_company)
        db.session.commit()
        return new_company.to_dict(), 201

    def put(self, company_id):
        data = request.get_json()
        company = MovingCompany.query.get(company_id)
        if company:
            company.name = data['name']
            company.address = data['address']
            company.phone_number = data['phone_number']
            company.email = data['email']
            db.session.commit()
            return company.to_dict(), 200
        return {'error': 'Company not found'}, 404

    def delete(self, company_id):
        company = MovingCompany.query.get(company_id)
        if company:
            db.session.delete(company)
            db.session.commit()
            return {}, 204
        return {'error': 'Company not found'}, 404

#  API
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ProfileResource, '/profiles', '/profiles/<int:profile_id>')
api.add_resource(ChecklistResource, '/checklists', '/checklists/<int:checklist_id>')
api.add_resource(InventoryResource, '/inventories', '/inventories/<int:inventory_id>')
api.add_resource(MoveResource, '/moves', '/moves/<int:move_id>')
api.add_resource(QuoteResource, '/quotes', '/quotes/<int:quote_id>')
api.add_resource(BookingResource, '/bookings', '/bookings/<int:booking_id>')
api.add_resource(NotificationResource, '/notifications', '/notifications/<int:notification_id>')
api.add_resource(CommunicationResource, '/communications', '/communications/<int:communication_id>')
api.add_resource(MovingCompanyResource, '/companies', '/companies/<int:company_id>')

if __name__ == '__main__':
    app.run(debug=True)
