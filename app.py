from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()
user_name = os.getenv("User_name")
Pass_word = os.getenv("Pass_word")
app = Flask(__name__)
host = os.environ.get('MONGODB_URI', f'mongodb://<{user_name}>:<{Pass_word}>@ds017688.mlab.com:17688/heroku_9ktnwzhl')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
users = db.users
items = db.items
carts = db.carts
inventories = db.inventory


@app.route('/')
def home_page():
    return redirect(url_for('user_login', user=None))


@app.route('/', methods=['POST'])
def user_home_page():
    if request.form.get('user_id') is not None:
        user_id = request.form.get('user_id')
        user = users.find_one({'_id': ObjectId(user_id)})
        return render_template('home_page.html', user=user, items=items.find())
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')

    user = users.find_one({
        '$and': [
            {'user_name': user_name},
            {'user_password': user_password}
            ]})

    try:
        if user['user_name'] == user_name and user['user_password'] == user_password:
            return render_template('home_page.html', user=user, items=items.find())
    except:
        return redirect(url_for('user_login'))


@app.route('/search', methods=['POST'])
def search():
    user_id = request.form.get('user_id')
    search = request.form.get('search')
    _items = items.find()
    user = users.find_one({'_id': ObjectId(user_id)})
    search_items = []
    for item in _items:
        if search.lower() in item['name'].lower():
            search_items.append(item)
    return render_template('home_page.html', user=user, items=search_items)


@app.route('/user_login')
def user_login():
    return render_template('user_login.html', user=None)


@app.route('/user_login/create')
def user_new_form():
    return render_template('user_create.html', user=None)


@app.route('/user_login/create', methods=['POST'])
def user_new_create():
    user = {
        'user_email': request.form.get('user_email'),
        'user_name': request.form.get('user_name'),
        'user_password': request.form.get('user_password'),
        'user_is_admin': False
    }
    users_id = users.insert_one(user).inserted_id
    return redirect(url_for('user_login'))


@app.route('/user/account', methods=['POST'])
def user_account():
    user_id = request.form.get('user_id')
    if request.form.get('submit') is not None:
        if request.form.get('admin_password') == '!admin':
            user_is_admin = True
            inventory = {'user_id': ObjectId(user_id)}
            inventory_id = inventories.insert_one(inventory).inserted_id
        else:
            user_is_admin = False
            inventory_id = None
        updated_user = {
            'user_email': request.form.get('user_email'),
            'user_name': request.form.get('user_name'),
            'user_password': request.form.get('user_password'),
            'user_is_admin': user_is_admin,
            'inventory': inventory_id
        }
        users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': updated_user}
        )
    user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('user_edit.html', user=user)

@app.route('/user/cart', methods=['POST'])
def user_cart():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    user_cart = carts.find({'user_id': ObjectId(user_id)})
    return render_template('user_cart.html', user=user, user_cart=user_cart)


@app.route('/user/cart/add', methods=['POST', 'GET'])
def user_cart_add():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    item_id = request.form.get('item_id')
    item = items.find_one({'_id': ObjectId(item_id)})
    new_cart_item = {
        'name': item['name'],
        'description': item['description'],
        'amount': 1,
        'image': item['image'],
        'item_id': ObjectId(item_id),
        'user_id': ObjectId(user_id)
    }
    carts.insert_one(new_cart_item)
    return redirect(url_for('user_home_page'), code=307)

@app.route('/user/cart/item', methods=['POST'])
def user_cart_item():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    cart_item_id = request.form.get('cart_item_id')
    cart_item = carts.find_one({'_id': ObjectId(cart_item_id)})
    if request.form.get('edited') is not None:
        new_cart_item = {
            'name': cart_item['name'],
            'description': cart_item['description'],
            'amount': request.form.get('amount'),
            'image': cart_item['image'],
            'item_id': ObjectId(cart_item['item_id']),
            'user_id': ObjectId(cart_item['user_id'])
        }
        carts.update_one({'_id': ObjectId(cart_item['_id'])}, {'$set': new_cart_item})
    if request.form.get('delete') is not None:
        carts.delete_one({'_id': ObjectId(cart_item['_id'])})
        return redirect(url_for('user_cart'), code=307)
    cart_item = carts.find_one({'_id': ObjectId(cart_item_id)})
    return render_template('user_cart_item.html', user=user, cart_item=cart_item)

@app.route('/user/cart/edit', methods=['POST'])
def user_cart_edit():
    user_id = request.form.get('user_id')
    cart_item = carts.find_one({'user_id': ObjectId(user_id)})
    new_cart_item = {
        'name': cart_item['name'],
        'description': cart_item['description'],
        'amount': request.form.get('amount'),
        'image': cart_item['image'],
        'item_id': ObjectId(cart_item['item_id']),
        'user_id': ObjectId(cart_item['user_id'])
    }
    carts.update_one({'_id': ObjectId(cart_item['_id'])}, {'$set': new_cart_item})
    return redirect(url_for('user_cart_item'))

@app.route('/user/cart/delete', methods=['POST'])
def user_cart_delete():
    cart_item_id = request.form.get('cart_item_id')
    carts.delete_one({'_id': ObjectId(cart_item_id)})
    return redirect(url_for('user_cart'), code=307)



@app.route('/<user_id>/delete')
def user_delete(user_id):
    _user = users.find_one({'_id': ObjectId(user_id)})
    user_inventory = inventories.find_one({'_id': ObjectId(_user['inventory'])})
    user_items = items.find({'inventory': ObjectId(_user['inventory'])})
    cart_items = carts.find({'user_id': ObjectId(_user['_id'])})
    for item in cart_items:
        carts.delete_one({'_id': ObjectId(item['_id'])})
    for item in user_items:
        items.delete_one({'_id': ObjectId(item['_id'])})
    inventories.delete_one({'_id': ObjectId(user_inventory['_id'])})
    users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('home_page'))


@app.route('/admin/accounts', methods=['POST'])
def admin_account_list():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    if request.form.get('_user_id') is not None:
        _user_id = request.form.get('_user_id')
        _user = users.find_one({'_id': ObjectId(_user_id)})
        user_inventory = inventories.find_one({'_id': ObjectId(_user['inventory'])})
        user_items = items.find({'inventory': ObjectId(_user['inventory'])})
        cart_items = carts.find({'user_id': ObjectId(_user['_id'])})
        for item in cart_items:
            carts.delete_one({'_id': ObjectId(item['_id'])})
        for item in user_items:
            items.delete_one({'_id': ObjectId(item['_id'])})
        inventories.delete_one({'_id': ObjectId(user_inventory['_id'])})
        users.delete_one({'_id': ObjectId(_user_id)})
    return render_template('admin_account_list.html', user=user, users=users.find())


@app.route('/admin/inventory', methods=['POST'])
def admin_inventory():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    inventory = inventories.find_one({'user_id': ObjectId(user_id)})
    if request.form.get('edit') is not None:
        item_id = request.form.get('item_id')
        updated_item = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'image': request.form.get('image'),
            'inventory': ObjectId(inventory['_id'])
        }
        items.update_one({'_id': ObjectId(item_id)}, {'$set': updated_item})
    if request.form.get('add') is not None:
        item = {
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'image': request.from.get('image'),
            'inventory': ObjectId(inventory['_id'])
        }
        items.insert_one(item)
    if request.form.get('delete') is not None:
        item_id = request.form.get('item_id')
        items.delete_one({'_id': ObjectId(item_id)})

    user_items = items.find({'inventory': ObjectId(inventory['_id'])})
    return render_template('admin_inventory.html', user=user, inventory=inventory, items=user_items)

@app.route('/admin/add/item', methods=['POST'])
def admin_edit_inventory():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('admin_add_item.html', user=user)

@app.route('/admin/edit/item', methods=['POST'])
def admin_edit_item():
    user_id = request.form.get('user_id')
    user = users.find_one({'_id': ObjectId(user_id)})
    inventory = inventories.find_one({'user_id': ObjectId(user_id)})
    item_id = request.form.get('item_id')
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('admin_edit_item.html', user=user, inventory=inventory, item=item)



@app.route('/kill')
def kill():
    _users = users.find()
    _items = items.find()
    _carts = carts.find()
    _inventories = inventories.find()
    for user in _users:
        users.delete_one({'_id': ObjectId(user['_id'])})
    for item in _items:
        items.delete_one({'_id': ObjectId(item['_id'])})
    for cart in _carts:
        carts.delete_one({'_id': ObjectId(cart['_id'])})
    for inventory in _inventories:
        inventories.delete_one({'_id': ObjectId(inventory['_id'])})
    return redirect(url_for('home_page'))



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
