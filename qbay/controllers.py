from flask import render_template, request, session, redirect
from qbay.models import login, User, register, update_user
from qbay.models import create_listing, update_listing, Listing 
from qbay.models import Listing, book_listing, Booking 
from qbay import app
from datetime import datetime


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between a user's browser and the end server. 
        Typically it is packed and stored in the browser cookies. 
        They will be past along between every request the browser made 
        to this services. Here we store the user object into the 
        session, so we can tell if the client has already login 
        in the following sessions.
        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='login failed')


@app.route('/')
@authenticate
def home(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals

    # display all the listing 
    listings = Listing.query.filter_by().all() 

    # display all the booking 
    bookings = Booking.query.filter_by(user_id=user.id).all()

    return render_template(
        'index.html', user=user, listings=listings, bookings=bookings)


@app.route('/register', methods=['GET'])
def register_get():
    # templates are stored in the templates folder
    return render_template('register.html', message='')


@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "The passwords do not match"
    else:
        # use backend api to register the user
        success = register(name, email, password)
        if not success:
            error_message = "Registration failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


@app.route('/listcreate', methods=['GET'])
def listcreate_get():
    return render_template('listcreate.html', message='')


@app.route('/listcreate', methods=['POST'])
def listcreate_post():
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    email = request.form.get('email')
    error_message = None

    # use backend api to create a listing
    success = create_listing(title, description, price, email)
    if not success:
        error_message = "Create listing failed."
    # if there is any error messages when registering new user
    # at the backend, go back to the create listing page.
    if error_message:
        return render_template('listcreate.html', message=error_message)
    else:
        return redirect('/')


@app.route('/listupdate', methods=['GET'])
def listupdate_get():
    return render_template('listupdate.html', message='')
 
 
@app.route('/listupdate', methods=['POST'])
def listupdate_post():
    new_title = request.form.get('new-title')
    old_title = request.form.get('old-title')
    description = request.form.get('description')
    price = int(request.form.get('price'))
    error_message = None
    
    try:
        update = update_listing(old_title, new_title, description, price)
    except IndexError:
        error_message = "Update listing failed."
        return render_template('listupdate.html', message=error_message)
        
    if not update:
        error_message = "Update listing failed."
       
    if error_message:
        return render_template('listupdate.html', message=error_message)
    else:
        return redirect('/')


@app.route('/profileupdate', methods=['GET'])
def profileupdate_get():
    email = session['logged_in']
    user = User.query.filter_by(email=email).one_or_none()
    return render_template('profileupdate.html', user=user, message='') 


@app.route('/profileupdate', methods=['POST'])
def profileupdate_post(): 
    email = session['logged_in']
    user = User.query.filter_by(email=email).one_or_none()
    user_id = user.id

    name = request.form.get('name')
    new_email = request.form.get('email')
    billing_address = request.form.get('billing_address')
    postal_code = request.form.get('postal_code')
    error_message = None
    
    # use backend api to update the user
    success = update_user(
        user_id, name, new_email, billing_address, postal_code)

    if not success:
        error_message = "Update failed."
    if error_message:
        return render_template(
            'profileupdate.html', user=user, message=error_message)
    else:
        return redirect('/') 


@app.route('/booking', methods=['GET'])
def booking_get():
    email = session['logged_in']
    user = User.query.filter_by(email=email).one_or_none()
    return render_template('booking.html', user=user, message='') 


@app.route('/booking', methods=['POST'])
def booking_post(): 
    email = session['logged_in']
    user = User.query.filter_by(email=email).one_or_none()
    user_id = user.id

    listing_id = request.form.get('listing_id') 
    cur_listing = Listing.query.filter_by(id=listing_id).one_or_none() 
    date = request.form.get('date') 
    error_message = None
    price = cur_listing.price
    date_object = datetime.strptime(date, '%m-%d-%Y').date()

    # use backend api to update the user
    success = book_listing(
        user_id, listing_id, price, date_object) 

    if not success:
        error_message = "Booking failed." 
    if error_message:
        return render_template(
            'booking.html', user=user, message=error_message)
    else:
        return redirect('/')