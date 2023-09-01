from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_user(request.form): # This is where we make sure that our form data is valid
        return redirect('/') # If form data is bad, we redirect to our home page and display the flash messages
    
    # If our form data is good, we use it to create user data
    
    data = {
        "username": request.form['username'],
        "password": request.form['password']
    }

    id = User.save(data) # A successful addition to our db returns the row number (id)

    session['user_id'] = id # We save the id in session. This acts as a login because we can now access the id of the logged in user

    return redirect('/dashboard') # We then redirect to our dashboard

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_username(request.form) # We use our form data to check if the user is in our database

    if not user: # If no user is found, we redirect to our home page and display a flash message
        flash("Invalid Username")
        return redirect('/')
    
    if user.password != request.form['password']: # If the password is wrong, we redirect to our home page and display a flash message
        flash("Invalid Password")
        return redirect('/')
    
    print(user.id)
    session['user_id'] = user.id # We save the id in session. This acts as a login because we can now access the id of the logged in user

    return redirect('/dashboard') # We then redirect to our dashboard

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: # We check if a user_id is present in session, which would mean that a user is logged in
        return redirect('/logout') # No user_id means we go to our logout route
    
    data = {
        'id': session['user_id'] # We get the user_id from session
    }

    user = User.get_by_id(data) # We pass the data to User.get_by_id to get the user from our database

    return render_template("dashboard.html", user=user) # We render our dashboard page and pass along the user info

@app.route('/logout')
def logout():
    session.clear() # Our logout route just clears session, which deletes the user_id logging the user out
    return redirect('/') # We don't render a page here. We simply redirect to our home page