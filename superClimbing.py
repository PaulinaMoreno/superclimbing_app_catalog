import httplib2
import json
import os
import requests
import random
import string
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash  # noqa: E402
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from models import Base, Category, Item, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from flask_uploads import (UploadSet, configure_uploads, IMAGES, patch_request_class, UploadNotAllowed)  # noqa
from flask_seasurf import SeaSurf


app = Flask(__name__)
csrf = SeaSurf(app)
# Initialize CSRF protection.
csrf.init_app(app)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Category Application"
DEFAULT = False

# Connect to Database and create database session
engine = create_engine('sqlite:///superclimbing.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Image uploads app config
app.config['UPLOADED_IMAGES_DEST'] = os.getcwd() + '/static/img/'
app.config['UPLOADED_IMAGES_URL'] = 'http://localhost:8000/static/img/'

# Upload image use flask_uploads
photos = UploadSet('images', IMAGES)
configure_uploads(app, photos)

# Create anti-forgery state token
# Exclude the view from CSRF validation.


@csrf.exempt
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    print state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Exclude the view from CSRF validation.


@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),  # noqa
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    print data['email']
    print user_id
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '  # noqa
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


@csrf.exempt
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


@csrf.exempt
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


@csrf.exempt
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
# DISCONNECT - Revoke a current user's token and reset their login_session
# Exclude the view from CSRF validation.


@csrf.exempt
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have successfully been logged out.")
        return redirect(url_for('superclimbing'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.',
                                 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category and Item Information
@app.route('/superclimbing/<int:category_id>/JSON')
def categoryListJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/superclimbing/JSON')
def categoriesJSON():
    categoryList = session.query(Category).all()
    return jsonify(categoriesList=[c.serialize for c in categoryList])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
def categoryItemsJSON(category_id, item_id):
    Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Item.serialize)


# Principal view
@app.route('/')
@app.route('/superclimbing/')
def superclimbing():
    # Get all categories
    categories = session.query(Category).order_by(asc(Category.name)).all()
    # Last 10 added items
    lastest_items = session.query(Item).order_by(desc(Item.id)).limit(10)
    username = "*"
    """Verify if user is logged and send this information as a parameter
    to decide what options are available to show"""

    if 'username' in login_session:
        username = login_session['username']
    return render_template('superclimbing.html', categories=categories,
                           lastest=lastest_items, username=username)


# Create a new category
@app.route('/superclimbing/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Verify if requested information is given
        c_name = request.form['name']
        c_description = request.form['description']
        c_image = request.files['category_image']
        if not (c_name and c_description and c_image):
            flash("You must fill in all the fields")
        else:
            # Get image name and url from upload file
            filename = photos.save(c_image)
            url = photos.url(filename)
            newCategory = Category(name=request.form['name'],
                                   description=request.form['description'],
                                   cat_image_filename=filename,
                                   cat_image_url=url,
                                   user_id=login_session['user_id'])
            session.add(newCategory)
            flash('New Category %s Successfully Created' % newCategory.name)
            session.commit()
        return redirect(url_for('superclimbing'))
    else:
        return render_template('new_category.html')


# Edit a category
@app.route('/superclimbing/category/<int:category_id>/edit/',
           methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['description']:
            editedCategory.description = request.form['description']
        if 'category_image' in request.files:
            # Remove previous image for file system
            os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'],
                                   editedCategory.cat_image_filename))
            # Get image name and url from upload file
            filename = photos.save(request.files['category_image'])
            url = photos.url(filename)
            editedCategory.cat_image_filename = filename
            editedCategory.cat_image_url = url
        session.add(editedCategory)
        session.commit()
        flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('superclimbing'))
    else:
        return render_template('edit_category.html', category=editedCategory)


# Delete a Category
@app.route('/superclimbing/category/<int:category_id>/delete/',
           methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('superclimbing'))
    else:
        return render_template('delete_category.html',
                               category=categoryToDelete)


@app.route('/superclimbing/category/<int:category_id>')
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('show_category.html',
                               category=category, username="*")
    return render_template('show_category.html',
                           category=category, username=creator)


# Create a new item
@app.route('/superclimbing/<int:category_id>/item/new/',
           methods=['GET', 'POST'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        # verify if requested information is gisven
        i_name = request.form['name']
        i_description = request.form['description']
        i_price = request.form['price']
        i_image = request.files['item_image']
        if not (i_name and i_description and i_image and i_price):
            flash("You must fill in all the fields")
        else:
            # get image name and url from upload file
            filename = photos.save(i_image)
            url = photos.url(filename)
            new_item = Item(name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            category_id=category.id,
                            item_image_filename=filename,
                            item_image_url=url,
                            user_id=category.user_id)
            session.add(new_item)
            flash('New Item %s Successfully Created' % new_item.name)
            session.commit()
            return redirect(url_for('superclimbing'))
    else:
            return render_template('new_item.html', category_id=category_id)


# Show all items per Category
@app.route('/superclimbing/category/<int:category_id>/items')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    category_items = session.query(Item).filter_by(category_id=category_id).all()  # noqa
    creator = getUserInfo(category.user_id)
    print category_items
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template('show_items.html',
                               items=category_items,
                               category=category, username="*")
    return render_template('show_items.html', category=category,
                           items=category_items, username=creator)


# Edit item
@app.route('/superclimbing/category/<int:category_id>/items/<int:item_id>/edit/',  # noqa
           methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=editedItem.category_id).one()  # noqa
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['category']:
            category_selected = session.query(Category).filter_by(
                              name=request.form['category']).one()
            editedItem.category_id = category_selected.id
        if 'item_image' in request.files:
            # Remove previous image for file system
            os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'],
                                   editedItem.item_image_filename))
            # Get image name and url from upload file
            filename = photos.save(request.files['item_image'])
            url = photos.url(filename)
            editedItem.item_image_filename = filename
            editedItem.item_image_url = url
        session.add(editedItem)
        session.commit()
        flash("Item Successfully Edited")
        return render_template('show_category.html', category=category)
    else:
        category = session.query(Category).filter_by(
                   id=editedItem.category_id).one()
        """ Get all possible categories to populate
        the select element in the html"""
        list_categories = session.query(Category).filter_by(user_id=category.user_id).all()  # noqa
        return render_template('edit_item.html', item=editedItem,
                               listCategories=list_categories)


# Delete an item
@app.route('/superclimbing/category/<int:category_id>/items/<int:item_id>/delete/',  # noqa
            methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=itemToDelete.category_id).one()  # noqa
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != category.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()'>"  # noqa
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Item Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('superclimbing'))
    else:
        return render_template('delete_item.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = "lYZs5h0W707E-pYaAi8ST-su"
    app.run(host='0.0.0.0', port=8000)
