#APP.PY
from flask import Flask, request, session, jsonify, redirect, url_for
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from config import db
from models import User, Profile, Checklist, Inventory, Move, Quote, Booking, Notification, Communication, MovingCompany
from datetime import datetime
import bcrypt

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
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')  # added role attribute

            if not username or not email or not password or not role:
                return {'error': 'Missing required fields'}, 400

            if User.query.filter_by(username=username).first():
                return {'error': 'Username already exists'}, 400

            if User.query.filter_by(email=email).first():
                return {'error': 'Email already exists'}, 400

            new_user = User(
                username=username,
                email=email,
                role=role
            )
            new_user.password = password  # This will hash the password

            db.session.add(new_user)
            db.session.commit()
            return new_user.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'error': 'Email and password are required'}, 400
        
        user = User.query.filter_by(email=email).first()
        if user and user.verify_password(password):
            session['user_id'] = user.id
            # Redirect based on user role
            if user.role == 'user':
                return {'message': 'Login successful', 'redirect': '/user_dashboard'}, 200
            elif user.role == 'company':
                return {'message': 'Login successful', 'redirect': '/company_dashboard'}, 200
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

# Moving Company Authentication and Management
class MovingCompanySignup(Resource):
    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            contact_email = data.get('email')
            contact_phone = data.get('phone_number')
            address = data.get('address')
            password = data.get('password')

            if not name or not contact_email or not contact_phone or not address or not password:
                return {'error': 'Missing required fields'}, 400

            new_company = MovingCompany(
                name=name,
                contact_email=contact_email,
                contact_phone=contact_phone,
                address=address
            )
            new_company.password = password  # This will hash the password

            db.session.add(new_company)
            db.session.commit()
            return new_company.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class MovingCompanyLogin(Resource):
    def post(self):
        data = request.get_json()
        company = MovingCompany.query.filter_by(contact_email=data['email']).first()
        if company and company.verify_password(data['password']):
            session['company_id'] = company.id
            return {'redirect': '/company_dashboard'}, 200
        return {'error': 'Invalid credentials'}, 401

class MovingCompanyLogout(Resource):
    def delete(self):
        session.pop('company_id', None)
        return {}, 204

class MovingCompanyCheckSession(Resource):
    def get(self):
        company_id = session.get('company_id')
        if company_id:
            company = MovingCompany.query.get(company_id)
            if company:
                return company.to_dict(), 200
        return {}, 204

# User Role-Based Dashboards
class UserDashboardResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user and user.role == 'user':
                return jsonify({'message': 'Welcome to User Dashboard', 'user': user.to_dict()})
        return redirect('/login')

class CompanyDashboardResource(Resource):
    def get(self):
        company_id = session.get('company_id')
        if company_id:
            company = MovingCompany.query.get(company_id)
            if company:
                return jsonify({'message': 'Welcome to Company Dashboard', 'company': company.to_dict()})
        return redirect('/login')

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
        required_keys = ['user_id', 'company_id', 'current_address', 'new_address', 'moving_date']
        if not all(key in data for key in required_keys):
            return {'error': 'Missing required fields'}, 400
        
        try:
            moving_date = datetime.strptime(data['moving_date'], '%Y-%m-%d')
        except ValueError:
            return {'error': 'Invalid date format'}, 400
        
        new_move = Move(
            user_id=data['user_id'],
            company_id=data['company_id'],
            moving_date=moving_date,
            current_address=data['current_address'],
            new_address=data['new_address'],
            special_requirements=data.get('special_requirements')
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
            move.moving_date = datetime.strptime(data['moving_date'], '%Y-%m-%d')
            move.current_address = data['current_address']
            move.new_address = data['new_address']
            move.special_requirements = data.get('special_requirements')
            
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
        status='pending'  # You can set the default status here
    )
        db.session.add(new_quote)
        db.session.commit()
        return new_quote.to_dict(), 201

    def put(self, quote_id):
        data = request.get_json()
        quote = Quote.query.get(quote_id)
        if quote:
            quote.move_id = data.get('move_id', quote.move_id)
            quote.price = data.get('price', quote.price)
            quote.status = data.get('status', quote.status)
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
    
    from datetime import datetime

    def post(self):
        data = request.get_json()
        new_booking = Booking(
            quote_id=data['quote_id'],
            customer_id=data['customer_id'],
            moving_company_id=data['moving_company_id'],
            move_id=data['move_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.to_dict(), 201

    def put(self, booking_id):
        data = request.get_json()
        booking = Booking.query.get(booking_id)
        if booking:
            booking.quote_id = data.get('quote_id', booking.quote_id)
            booking.customer_id = data.get('customer_id', booking.customer_id)
            booking.moving_company_id = data.get('moving_company_id', booking.moving_company_id)
            booking.move_id = data.get('move_id', booking.move_id)
            booking.date = datetime.strptime(data.get('date', booking.date), '%Y-%m-%d').date()
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
    def get(self, **kwargs):
        notification_id = kwargs.get('notification_id')
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
            booking_id=data['booking_id'],
            message=data['message'],
            timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
        )
        db.session.add(new_notification)
        db.session.commit()
        return new_notification.to_dict(), 201

    def put(self, notification_id):
        data = request.get_json()
        notification = Notification.query.get(notification_id)
        if notification:
            notification.booking_id = data.get('booking_id', notification.booking_id)
            notification.message = data.get('message', notification.message)
            notification.timestamp = datetime.strptime(data.get('timestamp', notification.timestamp), '%Y-%m-%dT%H:%M:%S')
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
    def get(self, **kwargs):
        communication_id = kwargs.get('communication_id')
        if communication_id:
            communication = Communication.query.get(communication_id)
            if communication:
                return communication.to_dict(only=['id', 'booking_id', 'message', 'timestamp']), 200
            return {'error': 'Communication not found'}, 404
        communications = Communication.query.all()
        return [communication.to_dict(only=['id', 'booking_id', 'message', 'timestamp']) for communication in communications], 200

    def post(self):
        data = request.get_json()
        new_communication = Communication(
            booking_id=data['booking_id'],
            message=data['message'],
            timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
        )
        db.session.add(new_communication)
        db.session.commit()
        return new_communication.to_dict(), 201

    def put(self, communication_id):
        data = request.get_json()
        communication = Communication.query.get(communication_id)
        if communication:
            communication.booking_id = data.get('booking_id', communication.booking_id)
            communication.message = data.get('message', communication.message)
            communication.timestamp = datetime.strptime(data.get('timestamp', communication.timestamp), '%Y-%m-%dT%H:%M:%S')
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

# Register Resources
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

api.add_resource(MovingCompanySignup, '/company_signup')
api.add_resource(MovingCompanyLogin, '/company_login')
api.add_resource(MovingCompanyLogout, '/company_logout')
api.add_resource(MovingCompanyCheckSession, '/company_check_session')

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ProfileResource, '/profiles', '/profiles/<int:profile_id>')
api.add_resource(ChecklistResource, '/checklists', '/checklists/<int:checklist_id>')
api.add_resource(InventoryResource, '/inventories', '/inventories/<int:inventory_id>')
api.add_resource(MoveResource, '/moves', '/moves/<int:move_id>')
api.add_resource(QuoteResource, '/quotes', '/quotes/<int:quote_id>')
api.add_resource(BookingResource, '/bookings', '/bookings/<int:booking_id>')
api.add_resource(NotificationResource, '/notifications', '/notifications/<int:notification_id>')
api.add_resource(CommunicationResource, '/communications', '/communications/<int:communication_id>')
api.add_resource(UserDashboardResource, '/user_dashboard')
api.add_resource(CompanyDashboardResource, '/company_dashboard')

