# Movers-BACK-END
The Movers App is a comprehensive web application designed to facilitate the process of moving for users and manage the moving services for moving companies. It provides functionalities for user authentication, move management, inventory tracking, and more.

# Features
User Management: Sign up, log in, and manage user profiles.
Moving Companies: Sign up and manage moving company details and authentication.
Checklists & Inventory: Create and manage moving checklists and inventory items.
Move Management: Schedule and manage moves, quotes, and bookings.
Notifications & Communications: Send and receive notifications and communications regarding moves.

# Technologies -Used
Flask: Web framework for building the application.
Flask-RESTful: Extension for building REST APIs.
Flask-Migrate: Handling database migrations.
Flask-CORS: Cross-Origin Resource Sharing support.
SQLAlchemy: ORM for database interactions.
SQLite: Database for storing application data.
bcrypt: Password hashing for security.

# Setup And Installation
# Prerequisites
.Python 3.x   
.pip

#  Installation
# 1 Clone the repository:
git clone: https://github.com/Tony-Muriuki/Movers-BACK-END.git

# 2 Create a virtual environment:
python -m venv venv

 # 3: Activate the virtual environment:

.On Windows: venv\Scripts\activate

.On macOS/Linux: source venv/bin/activate

# 4 Install the required dependencies:
pip install -r requirements.txt

# 5 Run database migrations:
flask db upgrade

# 6 Seed the database:
python seed.py

# 7 Start the Flask application:
python app.py


# API ENDPOINTS
User Management
Sign Up: POST /signup
Login: POST /login
Logout: DELETE /logout
Check Session: GET /check_session

# Moving Company Management
Company Sign Up: POST /company_signup
Company Login: POST /company_login
Company Logout: DELETE /company_logout
Check Company Session: GET /company_check_session

# User Resources
Get Users: GET /users
Get User by ID: GET /users/<user_id>
Update User: PUT /users/<user_id>

# Profile Resources
Get Profiles: GET /profiles
Get Profile by ID: GET /profiles/<profile_id>
Create Profile: POST /profiles
Update Profile: PUT /profiles/<profile_id>
Delete Profile: DELETE /profiles/<profile_id>

# Checklist Resources
Get Checklists: GET /checklists
Get Checklist by ID: GET /checklists/<checklist_id>
Create Checklist: POST /checklists
Update Checklist: PUT /checklists/<checklist_id>
Delete Checklist: DELETE /checklists/<checklist_id>

# Inventory Resources
Get Inventories: GET /inventories
Get Inventory by ID: GET /inventories/<inventory_id>
Create Inventory: POST /inventories
Update Inventory: PUT /inventories/<inventory_id>
Delete Inventory: DELETE /inventories/<inventory_id>

# Move Resources
Get Moves: GET /moves
Get Move by ID: GET /moves/<move_id>
Create Move: POST /moves
Update Move: PUT /moves/<move_id>
Delete Move: DELETE /moves/<move_id>

# Quote Resources
Get Quotes: GET /quotes
Get Quote by ID: GET /quotes/<quote_id>
Create Quote: POST /quotes
Update Quote: PUT /quotes/<quote_id>
Delete Quote: DELETE /quotes/<quote_id>

# Booking Resources
Get Bookings: GET /bookings
Get Booking by ID: GET /bookings/<booking_id>
Create Booking: POST /bookings
Update Booking: PUT /bookings/<booking_id>
Delete Booking: DELETE /bookings/<booking_id>

# Notification Resources
Get Notifications: GET /notifications
Get Notification by ID: GET /notifications/<notification_id>
Create Notification: POST /notifications
Update Notification: PUT /notifications/<notification_id>
Delete Notification: DELETE /notifications/<notification_id>

# Communication Resources
Get Communications: GET /communications
Get Communication by ID: GET /communications/<communication_id>
Create Communication: POST /communications
Update Communication: PUT /communications/<communication_id>
Delete Communication: DELETE /communications/<communication_id>

# Moving Company Resources
Get Companies: GET /companies
Get Company by ID: GET /companies/<company_id>
Update Company: PUT /companies/<company_id>
Delete Company: DELETE /companies/<company_id>

# Contributing
Feel free to submit issues or pull requests. If you have suggestions or improvements, we'd love to hear from you!

# Contact
For any questions, please contact kamandetonymuriuki@gmail.com