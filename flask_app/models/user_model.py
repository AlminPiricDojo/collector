from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import item_model # Import item_model to get access to the Item class

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.items = [] # This list will hold all Items created by a user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('collector-py').query_db(query)
        
        users = []
        for row in results:
            users.append(cls(row))

        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (%(username)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('collector-py').query_db(query, data) # Successful saves return the row number (id)
    
    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL('collector-py').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('collector-py').query_db(query,data)
        return cls(results[0])
    
    @staticmethod # We use the static method to perform checks on the user data coming from our form
    def validate_user(user): # user is just a dictionary at this point because it is coming from our form
        is_valid = True # is_valid starts at True, and only changes to False if one of the checks fails

        query = "SELECT * FROM users WHERE username = %(username)s;" # We look for the user by username

        results = connectToMySQL('collector-py').query_db(query,user) # We save the result our query to the 'result' variable

        if len(results) >= 1: # If a user with the provided username exists, our username is not unique
            flash("Username already taken.") # We save a flash message to session
            is_valid=False  # We set is_valid to False. This means that our validation has failed.
        if len(user['username']) < 3: # Here we check that the username is at least 3 characters long
            flash("Username name must be at least 3 characters")
            is_valid= False
        else:
            if user['username'][0].isnumeric(): # Checks if first character is a number
                flash("Username cannot start with a number")
                is_valid= False
        if len(user['password']) < 8: # Checks if our password is at least 8 characters long
            flash("Password must be at least 8 characters")
            is_valid= False
        if user['password'] != user['confirm']: # Compares the two passwords
            flash("Password do not match")
            is_valid= False

        return is_valid # We return True for a valid form and False for an invalid form
    
    @classmethod
    def get_user_items(cls, data):
        query = "SELECT * FROM users LEFT JOIN items ON users.id=items.user_id WHERE users.id=%(id)s" # Get all users and the items they have created
        results = connectToMySQL('collector-py').query_db(query, data) # We need to pass the user id into our query
        user = cls(results[0]) # 'user' now holds an instance of User
        for item in results: # We iterate through all items in our results
            item_data = {
                'id': item['items.id'], # We need to specify the table for attributes that are found in both tables (id, created_at, updated_at)
                'name': item['name'],
                'description': item['description'],
                'created_at': item['items.created_at'],
                'updated_at': item['items.updated_at'],
                'user_id': item['user_id'],
                'liked': None,
                'number_of_likes': None
            }
            this_item = item_model.Item(item_data) # Instantiate Item using the dictionary data
            user.items.append(this_item) # Add item object to user.items (the list we created earlier)
        return user # Return the user instance along with a full list of items