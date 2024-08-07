from datetime import datetime, date
from config import db, app
from models import User, Profile, Checklist, Inventory, Move, MovingCompany, Quote, Booking, Notification, Communication

def seed_data():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()

        # Create users
        user1 = User(username='john_doe', password='password1', email='john@example.com', role='user')
        user2 = User(username='jane_doe', password='password2', email='jane@company.com', role='company')

        # Add users to the session
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create moving company
        company1 = MovingCompany(user_id=user2.id, name='Best Movers', contact_email='contact@bestmovers.com', contact_phone='123-456-7890', address='123 Move St, Metropolis, Country')

        # Add moving company to the session
        db.session.add(company1)
        db.session.commit()

        # Create profiles for users
        profile1 = Profile(user_id=user1.id, first_name='John', last_name='Doe', phone_number='555-1234', preferences='Vegetarian')
        profile2 = Profile(user_id=user2.id, first_name='Jane', last_name='Smith', phone_number='555-5678', preferences='Pet-friendly')

        # Add profiles to the session
        db.session.add(profile1)
        db.session.add(profile2)
        db.session.commit()

        # Create checklists for users
        checklist1 = Checklist(user_id=user1.id, home_type='Apartment')
        checklist2 = Checklist(user_id=user2.id, home_type='House')

        # Add checklists to the session
        db.session.add(checklist1)
        db.session.add(checklist2)
        db.session.commit()

        # Create inventory items
        inventory1 = Inventory(checklist_id=checklist1.id, item_name='Sofa', status='Packed', notes='Living room sofa')
        inventory2 = Inventory(checklist_id=checklist1.id, item_name='Dining Table', status='Not Packed', notes='Dining table with 6 chairs')
        inventory3 = Inventory(checklist_id=checklist2.id, item_name='Bed', status='Packed', notes='King-size bed')
        inventory4 = Inventory(checklist_id=checklist2.id, item_name='Refrigerator', status='Packed', notes='Double door refrigerator')

        # Add inventory items to the session
        db.session.add(inventory1)
        db.session.add(inventory2)
        db.session.add(inventory3)
        db.session.add(inventory4)
        db.session.commit()

        # Create moves
        move1 = Move(user_id=user1.id, company_id=company1.id, current_address='456 Old St, Metropolis, Country', new_address='789 New St, Metropolis, Country', moving_date=date(2024, 8, 15))
        move2 = Move(user_id=user2.id, company_id=company1.id, current_address='321 Old Ave, Metropolis, Country', new_address='654 New Ave, Metropolis, Country', moving_date=date(2024, 8, 20))

        # Add moves to the session
        db.session.add(move1)
        db.session.add(move2)
        db.session.commit()

        # Create quotes
        quote1 = Quote(move_id=move1.id, price=500.00, status='Accepted')
        quote2 = Quote(move_id=move2.id, price=750.00, status='Pending')

        # Add quotes to the session
        db.session.add(quote1)
        db.session.add(quote2)
        db.session.commit()

        # Create bookings
        booking1 = Booking(
            quote_id=quote1.id,
            customer_id=user1.id,
            moving_company_id=company1.id,
            move_id=move1.id,
            date=date(2024, 8, 15)
        )
        booking2 = Booking(
            quote_id=quote2.id,
            customer_id=user1.id,  # Assuming booking for the same user for simplicity
            moving_company_id=company1.id,
            move_id=move2.id,
            date=date(2024, 8, 20)
        )

        # Add bookings to the session
        db.session.add(booking1)
        db.session.add(booking2)
        db.session.commit()

        # Create notifications
        notification1 = Notification(booking_id=booking1.id, message='Your move has been confirmed.', timestamp=datetime.now())
        notification2 = Notification(booking_id=booking2.id, message='Your move is pending confirmation.', timestamp=datetime.now())

        # Add notifications to the session
        db.session.add(notification1)
        db.session.add(notification2)
        db.session.commit()

        # Create communications
        communication1 = Communication(booking_id=booking1.id, message='Please make sure to pack all items before the moving date.', timestamp=datetime.now())
        communication2 = Communication(booking_id=booking2.id, message='Reminder: Your move date is approaching.', timestamp=datetime.now())

        # Add communications to the session
        db.session.add(communication1)
        db.session.add(communication2)
        db.session.commit()

        # Print success message
        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
