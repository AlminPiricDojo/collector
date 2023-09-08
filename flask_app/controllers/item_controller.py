from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_app.models.item_model import Item

from flask_app.models import user_model # We import user_model to get access to the User class

@app.route("/items/add", methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        return render_template("add_item.html")
    
    if not Item.validate_item(request.form): # This is where we make sure that our form data is valid
        return redirect('/items/add') # If form data is bad, we redirect to the add item page
    
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'user_id': request.form['user_id'] # The user id is pulled from the hidden input in our form
    }
    Item.save(data)

    return redirect("/dashboard")

@app.route("/items/<int:id>")
def show_item(id):
    item = Item.get_one(id)
    return render_template("view_item.html", item=item)

@app.route("/items/<int:id>/update", methods=['GET', 'POST'])
def update_item(id):
    if request.method == 'GET':
        item = Item.get_one(id)
        return render_template("update_item.html", item=item)
    
    if not Item.validate_item(request.form): # This is where we make sure that our form data is valid
        return redirect(f'/items/{id}/update') # If form data is bad, we redirect to the update item page
    
    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description']
    }
    item = Item.update(data)
    return redirect("/dashboard")

@app.route("/items/<int:id>/delete")
def delete_item(id):
    Item.delete(id)
    return redirect("/dashboard")