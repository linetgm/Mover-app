#!/usr/bin/env python3

from datetime import datetime
from App import app, db
from Models import User, Profile, Checklist, Inventory, Move, Quote, Booking, Notification, Communication, MovingCompany

with app.app_context():
    # Drop existing tables
    db.drop_all()
    # Create tables
    db.create_all()

    # Clear session
    db.session.remove()

    # Create some users with dummy passwords
    user1 = User(
        id='1',
        username='alice',
        email='alice@example.com'
    )
    user1.password = 'password1'

    user2 = User(
        id='2',
        username='bob',
        email='bob@example.com'
    )
    user2.password = 'password2'

    # Create some profiles
    profile1 = Profile(
        id='1',
        user_id='1',
        first_name='Alice',
        last_name='Johnson',
        phone_number='555-1234',
        preferences='None'
    )
    
    profile2 = Profile(
        id='2',
        user_id='2',
        first_name='Bob',
        last_name='Smith',
        phone_number='555-5678',
        preferences='None'
    )

    # Create some checklists
    checklist1 = Checklist(
        id='1',
        user_id='1',
        home_type='Apartment'
    )
    
    checklist2 = Checklist(
        id='2',
        user_id='2',
        home_type='House'
    )

    # Create some inventory items
    inventory1 = Inventory(
        id='1',
        checklist_id='1',
        item_name='TV',
        status='Packed',
        notes='Handle with care'
    )
    
    inventory2 = Inventory(
        id='2',
        checklist_id='2',
        item_name='Sofa',
        status='Not Packed',
        notes=''
    )

    # Create some moving companies
    company1 = MovingCompany(
        id='1',
        name='Fast Movers',
        contact_email='info@fastmovers.com',
        contact_phone='555-7890',
        rating=4.5,
        address='123 Main St'
    )
    
    company2 = MovingCompany(
        id='2',
        name='Quick Relocators',
        contact_email='info@quickrelocators.com',
        contact_phone='555-0123',
        rating=4.7,
        address='456 Elm St'
    )

    # Create some moves
    move1 = Move(
        id='1',
        user_id='1',
        company_id='1',
        current_address='123 Old St',
        new_address='456 New St',
        moving_date=datetime(2023, 7, 9).date(),
        special_requirements='None'
    )
    
    move2 = Move(
        id='2',
        user_id='2',
        company_id='2',
        current_address='789 Old St',
        new_address='012 New St',
        moving_date=datetime(2023, 7, 10).date(),
        special_requirements='Fragile items'
    )

    # Create some quotes
    quote1 = Quote(
        id='1',
        move_id='1',
        price=500.00,
        status='Pending'
    )
    
    quote2 = Quote(
        id='2',
        move_id='2',
        price=800.00,
        status='Accepted'
    )

    # Create some bookings
    booking1 = Booking(
        id='1',
        quote_id='1',
        move_date=datetime(2023, 7, 15).date(),
        move_time=datetime(2023, 7, 15, 9, 0).time(),
        confirmation_status='Confirmed'
    )
    
    booking2 = Booking(
        id='2',
        quote_id='2',
        move_date=datetime(2023, 7, 20).date(),
        move_time=datetime(2023, 7, 20, 10, 0).time(),
        confirmation_status='Pending'
    )

    # Create some notifications
    notification1 = Notification(
        id='1',
        booking_id='1',
        message='Your move is confirmed for 15th July at 9:00 AM',
        timestamp=datetime.now()
    )
    
    notification2 = Notification(
        id='2',
        booking_id='2',
        message='Your move is pending confirmation',
        timestamp=datetime.now()
    )

    # Create some communications
    communication1 = Communication(
        id='1',
        booking_id='1',
        message='Please confirm your packing status.',
        timestamp=datetime.now()
    )
    
    communication2 = Communication(
        id='2',
        booking_id='2',
        message='Will you require additional packing materials?',
        timestamp=datetime.now()
    )

    # Add the records to the session and commit them to the database
    db.session.add_all([
        user1, user2, profile1, profile2, checklist1, checklist2, inventory1, inventory2, 
        company1, company2, move1, move2, quote1, quote2, booking1, booking2, 
        notification1, notification2, communication1, communication2
    ])
    db.session.commit()

    print("Database seeded!")
