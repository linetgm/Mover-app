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
 