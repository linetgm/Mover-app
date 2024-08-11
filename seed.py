from app import create_app, db
from app.models import User, Mover, Inventory, Move, Message
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Drop all tables (if needed, for resetting)
    db.drop_all()

    # Create all tables
    db.create_all()

    # Create sample users
    admin = User(
        email='admin@example.com',
        password_hash=generate_password_hash('adminpassword'),
        role='Admin',
        approved=True
    )
    customer1 = User(
        email='customer1@example.com',
        password_hash=generate_password_hash('customerpassword'),
        role='Customer',
        approved=True
    )
    customer2 = User(
        email='customer2@example.com',
        password_hash=generate_password_hash('customerpassword'),
        role='Customer',
        approved=True
    )
    mover1 = User(
        email='mover1@example.com',
        password_hash=generate_password_hash('moverpassword'),
        role='Mover',
        approved=True
    )
    mover2 = User(
        email='mover2@example.com',
        password_hash=generate_password_hash('moverpassword'),
        role='Mover',
        approved=True
    )

    db.session.add_all([admin, customer1, customer2, mover1, mover2])
    db.session.commit()

    # Create sample movers
    mover_data1 = Mover(
        user_id=mover1.id,
        company_name='Mover Company 1',
        pricing='150',
        availability='Monday-Friday'
    )
    mover_data2 = Mover(
        user_id=mover2.id,
        company_name='Mover Company 2',
        pricing='200',
        availability='Monday-Saturday'
    )

    db.session.add_all([mover_data1, mover_data2])
    db.session.commit()

    # Create sample inventory for customer1
    inventory1 = Inventory(
        user_id=customer1.id,
        house_type='One Bedroom',
        items={
            "items": [
                {"name": "Bed", "quantity": 1},
                {"name": "Table", "quantity": 1},
                {"name": "Chair", "quantity": 4}
            ]
        }
    )
    
    db.session.add(inventory1)
    db.session.commit()

    # Create sample move for customer1
    move1 = Move(
        user_id=customer1.id,
        current_location='123 Old Street, Cityville',
        new_location='456 New Street, Townsville',
        moving_date=datetime.strptime('2024-09-15', '%Y-%m-%d'),
        status='Pending'
    )

    db.session.add(move1)
    db.session.commit()

    # Seed sample messages between customer1 and mover1
    message1 = Message(
        sender_id=customer1.id,
        receiver_id=mover1.id,
        move_id=move1.id,
        content='Hi, I would like to confirm the move on September 15th.',
        timestamp=datetime.utcnow()
    )
    message2 = Message(
        sender_id=mover1.id,
        receiver_id=customer1.id,
        move_id=move1.id,
        content='Sure, the move is confirmed for September 15th. We will arrive at 9 AM.',
        timestamp=datetime.utcnow()
    )

    db.session.add_all([message1, message2])
    db.session.commit()

    print("Database seeded successfully!")