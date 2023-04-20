from datetime import datetime
from qbay import app
from flask_sqlalchemy import SQLAlchemy 
from datetime import timedelta
import re 
'''
This file defines data models and related business logics
'''


db = SQLAlchemy(app)


# User entity to keep track of user information
class User(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(
        db.String(80), nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False)
    password = db.Column(
        db.String(120), nullable=False)
    billing_address = db.Column(
        db.String(50), default='')
    postal_code = db.Column(
        db.String(7), default='')
    balance = db.Column(
        db.Float, autoincrement=False, default=100)

    def __repr__(self):
        return '<User %r>' % self.username


# Bookings for listings
class Booking(db.Model): 
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False)
    listing_id = db.Column(
        db.Integer, db.ForeignKey('listing.id'), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(
        db.Float, nullable=False, default=0.0)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now()) 

    def __repr__(self): 
        return '<Booking %d>' % self.id


# Review for users to leave ratings on property listings
class Review(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(
        db.Integer, db.ForeignKey('listing.id'), nullable=False)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now())
    price = db.Column(
        db.Float, nullable=False)
    review_text = db.Column(
        db.String(300), nullable=False)


# Listing of a property
class Listing(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(
        db.String(100), nullable=False)
    description = db.Column(
        db.String(200), nullable=False)
    price = db.Column(
        db.Integer, nullable=False)
    last_modified_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now())
    owner_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(
        db.String(80))
    available = db.Column(
        db.Boolean)
    
    def __repr__(self): 
        return '<Listing %d>' % self.id

    
# create all tables
db.create_all()


def valid_username(username):
    '''
    Checks if the username is valid
      Parameters:
        username (string): user name
      Returns:
        True if username is valid otherwise False
    '''
    username_len = len(username)
    if not username.replace(" ", "").isalnum() or \
        username[0].isspace() or username[-1].isspace() \
            or username_len <= 2 or username_len >= 20: 
        return False
    return True


def valid_email(email):
    '''
    Checks if the email is valid
      Parameters:
        email (string): user email
      Returns:
        True if email is valid otherwise False
    '''
    regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if re.fullmatch(regex, email): 
        return True
    return False


def valid_password(password):
    '''
    Checks if the password is valid
      Parameters:
        password (string): user password
      Returns:
        True if password is valid otherwise False
    '''
    regex = re.compile(
        "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[#?!@$%^&*-]).{6,}$")
    if re.fullmatch(regex, password): 
        return True
    return False


def unique_id(id): 
    '''
    Check the uniqueness of the user id  
      Parameters:
        id (integer):     user id 
      Returns:
        True if it is unique otherwise False
    '''
    valids = User.query.filter_by(id=id).all()
    if len(valids) == 1: 
        return True 
    return False 


def valid_title(title):
    '''
    Checks if the title is valid
      Parameters:
        title (string): title of listing
      Returns:
        True if title is valid otherwise False
    '''
    title_len = len(title)
    if not title.replace(" ", "").isalnum() or \
        title[0].isspace() or title[-1].isspace() \
            or title_len > 80:
        return False
    return True


def valid_description(title, description):
    '''
    Checks if the description is valid
      Parameters:
        title (string): title of listing
        description (string): description of listing
      Returns:
        True if the description is valid otherwise False
    '''
    title_len = len(title)
    description_len = len(description)
    if description_len > 2000 or description_len < 20 or \
            description_len <= title_len:
        return False
    return True


def valid_date(date):
    '''
    Checks if the date is valid
      Parameters:
        date (datetime): date
      Returns:
        True if the date is valid otherwise False
    '''
    d1 = datetime(2021, 1, 2)
    d2 = datetime(2025, 1, 2)
    if date <= d1 or date >= d2:
        return False
    return True


def valid_price(price):
    '''
    Checks if the price is valid
      Parameters:
        price (Integer): price
      Returns:
        True if the price is valid otherwise False
    '''    
    if int(price) < 10 or int(price) > 10000:
        return False
    return True


def register(name, email, password):
    '''
    Register a new user
      Parameters:
        name (string):     user name
        email (string):    user email
        password (string): user password
      Returns:
        True if registration succeeded otherwise False
    '''
    # check if the email has been used:
    existed = User.query.filter_by(email=email).all()
    if len(existed) > 0:
        return False

    # check if email is valid 
    # email has to follow addr-spec defined in RFC5322
    if not valid_email(email): 
        return False 

    # check if name is valid 
    # greater than 2 and less than 20 
    # alphanumeric only 
    # space is not allowed as the prefix or suffix
    if not valid_username(name): 
        return False 

    # check if password is valid 
    # minimum length is 6 
    if not valid_password(password): 
        return False 

    # create a new user
    user = User(username=name, email=email, password=password)
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return True


def login(email, password):
    '''
    Check login information
      Parameters:
        email (string):    user email
        password (string): user password
      Returns:
        The user object if login succeeded otherwise None
    '''

    # Check if input meets the email/password requirements
    if not valid_email(email) or not valid_password(password):
        return None

    valids = User.query.filter_by(email=email, password=password).all()
    if len(valids) != 1:
        return None
    return valids[0]


def update_user(user_id, username, email, address, postal_code):
    '''
    Update user's name, user email, address, and postal code
      Parameters:
        user_id (integer):      user id
        username (string):      user name
        email (string):         user email
        address (string):       user billing address
        postal_code (string):   user postal code
      Returns:
        True if the user was able to update their information, otherwise False
    '''

    # Making sure postal code is non-empty and alphanumeric-only
    if len(postal_code) == 0 or not postal_code.replace(" ", "").isalnum():
        return False

    # Checking that postal code is valid Candian postal code
    regex = re.compile(
        "^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] [0-9][A-Z][0-9]$")
    if not re.fullmatch(regex, postal_code): 
        return False

    # Checking to see if the user name follows the requirements
    if not valid_username(username):
        return False

    # Find user with the email, and update their information accordingly
    user = User.query.filter_by(id=user_id).all()
    user[0].username = username
    user[0].postal_code = postal_code
    # Updating billing address if length is greater than 0
    if len(address) > 0:
        user[0].billing_address = address
    # Updating email if it is non-empty and valid
    if not valid_email(email) and len(email) > 0:
        return False
    elif len(email) > 0: 
        user[0].email = email
    db.session.commit()
    return True


def create_listing(title, description, price, email):
    '''
    Create listing
      Parameters:
        title (string): title of listing
        description (string): description of listing
        price (Integer) : price of listing
        email (string) : email of listing owner
      Returns:
        True if listing was created otherwise False
    '''

    # check if the title has been used:
    existed1 = Listing.query.filter_by(title=title).all()
    if len(existed1) > 0:
        return False

    # check if owner email exists in database:
    existed2 = User.query.filter_by(email=email).all()
    if len(existed2) < 1:
        return False

    # check if date is valid:
    if not valid_date(datetime.now()):
        return False

    # check if title meets requirements
    if not valid_title(title):
        return False

    # check if description meets requirements
    if not valid_description(title, description):
        return False

    # check if price meets requirements
    if not valid_price(price):
        return False

    # create a new listing
    listing = Listing(
        title=title, description=description, 
        price=price, owner_id=existed2[0].id,
        last_modified_date=datetime.now())

    # add it to the current database session
    db.session.add(listing)
    # actually save the user object
    db.session.commit()

    return True


def update_listing(old_title, new_title, description, price):
    '''
    Update listing's title, description, and price
      Parameters:
        old_title (string): existing listing title
        new_titletitle (string): listing title
        description (string): listing description
        price (string): listing price
      Returns:
        True if the user was able to update lisitng otherwise False
    '''
    
    # check if input meets the 
    # title/description/price requirements
    if not valid_title(new_title) or \
        not valid_description(new_title, description) or \
            not valid_price(price):
        return False

    # find listing with title, and update listing
    listing = Listing.query.filter_by(title=old_title).all()
    listing[0].title = new_title
    listing[0].description = description

    # update price if valid
    if listing[0].price > price:
        return False
    listing[0].price = price

    # update last_modified_date
    listing[0].last_modified_date = datetime.now()
    db.session.commit()
    return True


def book_listing(user_id, listing_id, price, date):
    '''
    Update listing's title, description, and price
      Parameters:
        user_id (integer): id of the current user
        listing_id (integer): booking id
        price (float): price of booking
        dates (datetime): date of booking
      Returns:
        True if the user was able to book listing otherwise False
    '''

    # User cannot book listing for his/her listing
    current_user = User.query.filter_by(id=user_id).all()
    listing_user = Listing.query.filter_by(id=listing_id).all()

    if len(current_user) < 1 or len(listing_user) < 1:
        return False

    if current_user[0].id == listing_user[0].owner_id:
        return False

    # User cannot book a listing that costs more than his/her balance
    if price > current_user[0].balance:
        return False

    # User cannot book a listing that is already booked 
    # with the overlapped dates
    date_end = date + timedelta(days=1)
    if len(
            Booking.query.filter(Booking.listing_id == listing_id, 
                                 Booking.date >= date, Booking.date 
                                 < date_end).all()) > 0:
        return False
    
    # Update the users current cash and make the listing unavailable
    current_user[0].balance -= price

    # Add the new booking
    booking = Booking(
        listing_id=listing_id, user_id=user_id, price=price, date=date)
    # add it to the current database session
    db.session.add(booking)
    # actually save the user object
    db.session.commit()
    return True