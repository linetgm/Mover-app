from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
import bcrypt
import re
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String, nullable=False)  # 'user' or 'company'

    # Relationships
    profiles = db.relationship('Profile', back_populates='user', cascade='all, delete-orphan')
    checklists = db.relationship('Checklist', back_populates='user', cascade='all, delete-orphan')
    moves = db.relationship('Move', back_populates='user', cascade='all, delete-orphan')
    company = db.relationship('MovingCompany', back_populates='user', uselist=False, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='customer', cascade='all, delete-orphan')

    serialize_rules = (
        '-password_hash',  # Exclude password hash
        '-profiles',  # Exclude user profiles from serialization
        '-checklists',  # Exclude user checklists from serialization
        '-moves',  # Exclude user moves from serialization
        '-company',  # Exclude user company from serialization
        '-bookings'  # Exclude user bookings from serialization
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.role:
            self.validate_role(None, self.role)
        if self.email:
            self.validate_email(None, self.email)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be provided.")
        if User.query.filter_by(username=username).first():
            raise ValueError("Username must be unique.")
        return username

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['user', 'company']:
            raise ValueError("Role must be either 'user' or 'company'.")
        return role

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email must be provided.")
        
        email_regex = r'^[\w\.-]+@[\w\.-]+$'
        if not re.match(email_regex, email):
            raise ValueError("Email format is invalid.")
        
        if User.query.filter_by(email=email).first():
            raise ValueError("Email must be unique.")
        
        if self.role == 'user':
            if not email.endswith('@example.com'):
                raise ValueError("User email must end with '@example.com'.")
        elif self.role == 'company':
            if not email.endswith('@company.com'):
                raise ValueError("Company email must end with '@company.com'.")
        
        return email


class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    preferences = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='profiles')

    serialize_rules = (
        '-user'  # Exclude user from serialization
        'id',
        'user_id',
        'first_name',
        'last_name',
        'phone_number',
        'preferences'
    )

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return name



class Checklist(db.Model, SerializerMixin):
    __tablename__ = 'checklists'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    home_type = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='checklists')
    inventory_items = db.relationship('Inventory', back_populates='checklist', cascade='all, delete-orphan')

    serialize_rules = (
        '-user',  # Exclude user from serialization
        '-inventory_items',  # Exclude inventory items from serialization
    )

    @validates('home_type')
    def validate_home_type(self, key, home_type):
        if not home_type:
            raise ValueError("Home type must be provided.")
        return home_type



class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)

    checklist = db.relationship('Checklist', back_populates='inventory_items')

    serialize_rules = (
        '-checklist',  # Exclude checklist from serialization
    )
    @validates('item_name', 'status')
    def validate_item(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value


class Move(db.Model, SerializerMixin):
    __tablename__ = 'moves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('moving_companies.id'), nullable=False)
    current_address = db.Column(db.String, nullable=False)
    new_address = db.Column(db.String, nullable=False)
    moving_date = db.Column(db.Date, nullable=False)
    special_requirements = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='moves')
    company = db.relationship('MovingCompany', back_populates='moves')
    quotes = db.relationship('Quote', back_populates='move', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='move', cascade='all, delete-orphan')

    serialize_rules = (
        '-user',  # Exclude user from serialization
        '-company',  # Exclude company from serialization
        '-quotes',  # Exclude quotes from serialization
        '-bookings'  # Exclude bookings from serialization
    )
    @validates('current_address', 'new_address', 'moving_date')
    def validate_move(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value



class Quote(db.Model, SerializerMixin):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    move_id = db.Column(db.Integer, db.ForeignKey('moves.id'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String, nullable=False)

    move = db.relationship('Move', back_populates='quotes')
    bookings = db.relationship('Booking', back_populates='quote', cascade='all, delete-orphan')

    serialize_rules = (
        '-move',  # Exclude move from serialization
        '-bookings'  # Exclude bookings from serialization
    )


    @validates('price', 'status')
    def validate_quote(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value

    


class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    moving_company_id = db.Column(db.Integer, db.ForeignKey('moving_companies.id'), nullable=False)
    move_id = db.Column(db.Integer, db.ForeignKey('moves.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    quote = db.relationship('Quote', back_populates='bookings')
    customer = db.relationship('User', back_populates='bookings')
    moving_company = db.relationship('MovingCompany', back_populates='bookings')
    move = db.relationship('Move', back_populates='bookings')
    notifications = db.relationship('Notification', back_populates='booking')
    communications = db.relationship('Communication', back_populates='booking')

    serialize_rules = (
        '-quote',  # Exclude quote from serialization
        '-customer',  # Exclude customer from serialization
        '-moving_company',  # Exclude moving company from serialization
        '-move',  # Exclude move from serialization
        '-notifications',  # Exclude notifications from serialization
        '-communications'  # Exclude communications from serialization
    )


    @validates('quote_id', 'customer_id', 'moving_company_id', 'move_id', 'date')
    def validate_booking(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value



class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    booking = db.relationship('Booking', back_populates='notifications')

    serialize_rules = (
        '-booking',  # Exclude booking from serialization
    )

    @validates('message', 'timestamp')
    def validate_notification(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value



class Communication(db.Model, SerializerMixin):
    __tablename__ = 'communications'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    booking = db.relationship('Booking', back_populates='communications')

    serialize_rules = (
        # '-booking.communications',  # Exclude booking communications from serialization
        '-booking'  # Exclude booking from serialization
    )

    @validates('message', 'timestamp')
    def validate_communication(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value



class MovingCompany(db.Model, SerializerMixin):
    __tablename__ = 'moving_companies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='company')
    moves = db.relationship('Move', back_populates='company')
    bookings = db.relationship('Booking', back_populates='moving_company')

    serialize_rules = (
        '-user',  # Exclude user from serialization
        '-moves',  # Exclude moves from serialization
        '-bookings'  # Exclude bookings from serialization
    )

    @validates('name', 'contact_email', 'contact_phone', 'address')
    def validate_moving_company(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value

