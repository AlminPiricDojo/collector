from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import user_model # We import user_model to get access to the User class

class Item:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None # This will hold an instance of User (the user who created the item)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM items LEFT JOIN users ON items.user_id=users.id;" # Get all items and the user who created each one
        results = connectToMySQL('collector-py').query_db(query)

        items = [] # This list will hold all items that come back from the db

        for row in results:
            this_item = cls(row) # Create an Item instance using the dictionary data from each row in the db

            user_data = {
                'id': row['user_id'],
                'username': row['username'],
                'password': row['password'],
                'created_at': row['users.created_at'], # We need to specify the table when a column is present in more than one table
                'updated_at': row['users.updated_at']
            }
            this_item.user = user_model.User(user_data) # Instantiate the user and associate them with each item

            items.append(this_item) # Add item (along with the user) to our list of items

        return items # Return the full list of items
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO items (name, description, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('collector-py').query_db(query, data)
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM items LEFT JOIN users ON items.user_id=users.id WHERE items.id=%(id)s"
        results = connectToMySQL('collector-py').query_db(query, {'id':id})

        this_item = cls(results[0]) # Instantiate the item using the data from the db

        user_data = {
            'id': results[0]['user_id'],
            'username': results[0]['username'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'], # We need to specify the table when a column is present in more than one table
            'updated_at': results[0]['users.updated_at']
        }
        
        this_item.user = user_model.User(user_data) # Instantiate the user and associate them with the item

        return this_item # Return the instance of the item (along with the user)