from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
import bcrypt

# Define the User model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    profiles = db.relationship('Profile', back_populates='user', cascade='all, delete-orphan')
    checklists = db.relationship('Checklist', back_populates='user', cascade='all, delete-orphan')
    moves = db.relationship('Move', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-password_hash', '-profiles.user', '-checklists.user', '-moves.user')

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
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            raise ValueError("Username must be unique.")
        
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email must be provided.")
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise ValueError("Email must be unique.")
        
        return email
 
 
 # Define the Profile model
class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profiles'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    preferences = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='profiles')

    serialize_rules = ('-user.profiles',)

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return name

# Define the Checklist model
class Checklist(db.Model, SerializerMixin):
    __tablename__ = 'checklists'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    home_type = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='checklists')
    inventory_items = db.relationship('Inventory', back_populates='checklist', cascade='all, delete-orphan')

    serialize_rules = ('-user.checklists', '-inventory_items.checklist')

    @validates('home_type')
    def validate_home_type(self, key, home_type):
        if not home_type:
            raise ValueError("Home type must be provided.")
        return home_type


# Define the Inventory model
class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'
    id = db.Column(db.String, primary_key=True)
    checklist_id = db.Column(db.String, db.ForeignKey('checklists.id'), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)

    checklist = db.relationship('Checklist', back_populates='inventory_items')

    serialize_rules = ('-checklist.inventory_items',)

    @validates('item_name', 'status')
    def validate_item(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value
    
# Define the Quote model
class Quote(db.Model, SerializerMixin):
    __tablename__ = 'quotes'
    id = db.Column(db.String, primary_key=True)
    move_id = db.Column(db.String, db.ForeignKey('moves.id'), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    status = db.Column(db.String, nullable=False)

    move = db.relationship('Move', back_populates='quotes')
    bookings = db.relationship('Booking', back_populates='quote', cascade='all, delete-orphan')

    serialize_rules = ('-move.quotes', '-bookings.quote')

    @validates('price', 'status')
    def validate_quote(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value
    
# Define the Booking model
class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'
    id = db.Column(db.String, primary_key=True)
    quote_id = db.Column(db.String, db.ForeignKey('quotes.id'), nullable=False)
    move_date = db.Column(db.Date, nullable=False)
    move_time = db.Column(db.Time, nullable=False)
    confirmation_status = db.Column(db.String, nullable=False)

    quote = db.relationship('Quote', back_populates='bookings')
    notifications = db.relationship('Notification', back_populates='booking', cascade='all, delete-orphan')
    communications = db.relationship('Communication', back_populates='booking', cascade='all, delete-orphan')

    serialize_rules = ('-quote.bookings', '-notifications.booking', '-communications.booking')

    @validates('move_date', 'move_time', 'confirmation_status')
    def validate_booking(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value

# Define the Notification model
class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    id = db.Column(db.String, primary_key=True)
    booking_id = db.Column(db.String, db.ForeignKey('bookings.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    booking = db.relationship('Booking', back_populates='notifications')

    serialize_rules = ('-booking.notifications',)

    @validates('message', 'timestamp')
    def validate_notification(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value
    
# Define the Communication model
class Communication(db.Model, SerializerMixin):
    __tablename__ = 'communications'
    id = db.Column(db.String, primary_key=True)
    booking_id = db.Column(db.String, db.ForeignKey('bookings.id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    booking = db.relationship('Booking', back_populates='communications')

    serialize_rules = ('-booking.communications',)

    @validates('message', 'timestamp')
    def validate_communication(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value
    
# Define the MovingCompany model
class MovingCompany(db.Model, SerializerMixin):
    __tablename__ = 'moving_companies'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact_email = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String, nullable=False)
    rating = db.Column(db.Numeric, nullable=True)
    address = db.Column(db.String, nullable=False)

    moves = db.relationship('Move', back_populates='company')

    serialize_rules = ('-moves.company',)

    @validates('name', 'contact_email', 'contact_phone', 'address')
    def validate_moving_company(self, key, value):
        if not value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be provided.")
        return value