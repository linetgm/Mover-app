#!/usr/bin/env python3
# seed.py
from datetime import datetime
from App import app, db
from Models import User, Profile, Checklist, Inventory, Move, Quote, Booking, Notification, Communication, MovingCompany
import random

with app.app_context():
    # Drop existing tables
    db.drop_all()
    # Create tables
    db.create_all()

    # Clear session
    db.session.remove()

    # Helper function to create a user
    def create_user(id, username, email, password):
        user = User(id=id, username=username, email=email)
        user.password = password
        return user

    # Create some users with hashed passwords
    users = [
        create_user(id='1', username='alice', email='alice@example.com', password='password1'),
        create_user(id='2', username='bob', email='bob@example.com', password='password2'),
        create_user(id='3', username='carol', email='carol@example.com', password='password3'),
        create_user(id='4', username='dave', email='dave@example.com', password='password4')
    ]

    # Create some profiles
    profiles = [
        Profile(id='1', user_id='1', first_name='Alice', last_name='Johnson', phone_number='555-1234', preferences='None'),
        Profile(id='2', user_id='2', first_name='Bob', last_name='Smith', phone_number='555-5678', preferences='None'),
        Profile(id='3', user_id='3', first_name='Carol', last_name='Williams', phone_number='555-9101', preferences='Allergies: Dust'),
        Profile(id='4', user_id='4', first_name='Dave', last_name='Brown', phone_number='555-1122', preferences='None')
    ]

    # List of valid home types
    home_types = [
        'Bedsitter',
        'One Bedroom',
        'Studio',
        'Two Bedroom'
    ]

    # Create checklists
    checklists = [
        Checklist(id='1', user_id='1', home_type=random.choice(home_types)),
        Checklist(id='2', user_id='2', home_type=random.choice(home_types)),
        Checklist(id='3', user_id='3', home_type=random.choice(home_types)),
        Checklist(id='4', user_id='4', home_type=random.choice(home_types))
    ]

    # Create some inventory items
    inventories = [
        Inventory(id='1', checklist_id='1', item_name='TV', status='Packed', notes='Handle with care'),
        Inventory(id='2', checklist_id='2', item_name='Sofa', status='Not Packed', notes=''),
        Inventory(id='3', checklist_id='3', item_name='Dining Table', status='Packed', notes='Disassemble legs'),
        Inventory(id='4', checklist_id='4', item_name='Bed Frame', status='Packed', notes='Mattress in separate box')
    ]

    # Create some moving companies
    moving_companies = [
        MovingCompany(id='1', name='Fast Movers', contact_email='info@fastmovers.com', contact_phone='555-7890', address='123 Main St', password='company1password'),
        MovingCompany(id='2', name='Quick Relocators', contact_email='info@quickrelocators.com', contact_phone='555-0123', address='456 Elm St', password='company2password'),
        MovingCompany(id='3', name='Reliable Movers', contact_email='contact@reliablemovers.com', contact_phone='555-3456', address='789 Oak St', password='company3password'),
        MovingCompany(id='4', name='Speedy Shifters', contact_email='info@speedyshifters.com', contact_phone='555-6543', address='101 Pine St', password='company4password')
    ]

    # Create some moves
    moves = [
        Move(id='1', user_id='1', company_id='1', current_address='123 Old St', new_address='456 New St', moving_date=datetime(2023, 7, 9).date(), special_requirements='None'),
        Move(id='2', user_id='2', company_id='2', current_address='789 Old St', new_address='012 New St', moving_date=datetime(2023, 7, 10).date(), special_requirements='Fragile items'),
        Move(id='3', user_id='3', company_id='3', current_address='234 Maple Ave', new_address='567 Birch Rd', moving_date=datetime(2023, 7, 11).date(), special_requirements='Extra packing materials'),
        Move(id='4', user_id='4', company_id='4', current_address='345 Cedar Dr', new_address='678 Spruce St', moving_date=datetime(2023, 7, 12).date(), special_requirements='Assistance with heavy items')
    ]

    # Create some quotes
    quotes = [
        Quote(id='1', move_id='1', price=500.00, status='Pending'),
        Quote(id='2', move_id='2', price=800.00, status='Accepted'),
        Quote(id='3', move_id='3', price=600.00, status='Pending'),
        Quote(id='4', move_id='4', price=750.00, status='Accepted')
    ]

    # Create some bookings
    bookings = [
        Booking(id='1', quote_id='1', move_date=datetime(2023, 7, 15).date(), move_time=datetime(2023, 7, 15, 9, 0).time(), confirmation_status='Confirmed'),
        Booking(id='2', quote_id='2', move_date=datetime(2023, 7, 20).date(), move_time=datetime(2023, 7, 20, 10, 0).time(), confirmation_status='Pending'),
        Booking(id='3', quote_id='3', move_date=datetime(2023, 7, 25).date(), move_time=datetime(2023, 7, 25, 11, 0).time(), confirmation_status='Confirmed'),
        Booking(id='4', quote_id='4', move_date=datetime(2023, 7, 30).date(), move_time=datetime(2023, 7, 30, 12, 0).time(), confirmation_status='Pending')
    ]

    # Create some notifications
    notifications = [
        Notification(id='1', booking_id='1', message='Your move is confirmed for 15th July at 9:00 AM', timestamp=datetime.now()),
        Notification(id='2', booking_id='2', message='Your move is pending confirmation', timestamp=datetime.now()),
        Notification(id='3', booking_id='3', message='Your move is confirmed for 25th July at 11:00 AM', timestamp=datetime.now()),
        Notification(id='4', booking_id='4', message='Your move is pending confirmation', timestamp=datetime.now())
    ]

    # Create some communications
    communications = [
        Communication(id='1', booking_id='1', message='Please confirm your packing status.', timestamp=datetime.now()),
        Communication(id='2', booking_id='2', message='Will you require additional packing materials?', timestamp=datetime.now()),
        Communication(id='3', booking_id='3', message='Please provide your new address for delivery confirmation.', timestamp=datetime.now()),
        Communication(id='4', booking_id='4', message='Do you need any assistance with packing?', timestamp=datetime.now())
    ]

    # Add all records to the session
    db.session.add_all(users + profiles + checklists + inventories + moving_companies + moves + quotes + bookings + notifications + communications)
    
    # Commit the transaction
    db.session.commit()

    print("Database seeded!")
