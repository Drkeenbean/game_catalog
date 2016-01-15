from app import app
from flask import render_template, url_for, \
    request, redirect, jsonify, make_response, flash
from flask import session as login_session
from models import Base, Item, Genre, Platform, User
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import random
import string
import json
import requests
from oauth2client import client

CLIENT_SECRET_FILE = 'client_secret.json'

# To use SQLite instead of postgresql, uncomment this line
# and delete or comment the following line
# engine = create_engine('sqlite:///game_catalog.db')
engine = create_engine('postgresql:///game_catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Constants to store genres and platforms
# for use in navigation menus
GENRES = session.query(Genre).order_by(Genre.name)
PLATFORMS = session.query(Platform).order_by(Platform.name)


@app.route('/login')
def login():
    # Create a random state token to prevent request forgery
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for x in xrange(64)
    )
    # Store state token in login_session for later use
    login_session['state'] = state
    template = render_template(
        'login.html',
        state=login_session['state'],
        title="Login",
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
    )
    return template


@app.route('/gsignin', methods=["POST"])
def gSignIn():
    # Verify that the state token sent from the login
    # page is the same as the state token stored in
    # login_session
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store google authorization code and use it
    # to get user credentials
    auth_code = request.data
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        auth_code
    )

    # Get user info from google with stored credentials
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    # Get user info from returned data and store in login_session
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']

    # Get user id from database
    # If None returned, add new user to datbase
    # from data stored in login_session
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Formats output to be returned as 'result' in login.html
    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 100px; height: 100px; border-radius: 100%;">'

    return output


@app.route('/gsignout')
def gSignOut():
    # Delete the login_session and redirect to home page
    del login_session['user_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    flash('User signed out')

    return redirect(url_for('index'))


@app.route('/')
def index():
    # Get most recent items from the database
    # to display on front page
    recentItems = session.query(Item).order_by(desc(Item.id)).limit(5)
    if 'username' not in login_session:
        # If user not logged in render public template
        template = render_template(
            'indexPublic.html',
            items=recentItems,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )
    else:
        # Render private template
        template = render_template(
            'index.html',
            items=recentItems,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )
    return template


@app.route('/item/new', methods=["POST", "GET"])
def newItem():
    if 'username' not in login_session:
        # If user not logged in, flash error message and
        # redirect to index
        flash("You must be logged in to add items.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Create new item and save to database
        newItem = Item(
            title=request.form['title'],
            description=request.form['description'],
            picture=request.form['picture'],
            genre_id=request.form['genre'],
            platform_id=request.form['platform'],
            user_id=login_session['user_id']
        )
        session.add(newItem)
        session.commit()

        flash("%s added!" % request.form['title'])

        return redirect(url_for('index'))
    else:
        return render_template(
            'newItem.html',
            title="Add new item",
            genres=GENRES.all(),
            platforms=PLATFORMS.all())


@app.route('/item/<int:item_id>')
def showItem(item_id):
    item = session.query(Item).get(item_id)
    owner = item.user_id
    if 'user_id' in login_session and login_session['user_id'] is owner:
        # Check if currently logged-in user
        # is owner of item and render page
        # with delete/edit buttons
        template = render_template(
            'item.html',
            item=item,
            title=item.title,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )
    else:
        # Render item public page
        template = render_template(
            'itemPublic.html',
            item=item,
            title=item.title,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )
    return template

# API endpoint views
# XML endpoints


@app.route('/recents_xml')
def showRecentXML():
    recentItems = session.query(Item).order_by(desc(Item.id)).limit(5)

    # Store template to make response
    # set response headers to XML to force
    # returned template to display as an XML tree
    template = render_template('recents.xml', items=recentItems)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


@app.route('/item/<int:item_id>_xml')
def showItemXML(item_id):
    item = session.query(Item).get(item_id)
    template = render_template('item.xml', item=item)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response
# end XML endpoint views

# JSON endpoints


@app.route('/recents_JSON')
def showRecentJSON():
    recentItems = session.query(Item).order_by(desc(Item.id)).limit(5)
    return jsonify(RecentItems=[i.serialize for i in recentItems])


@app.route('/item/<int:item_id>_JSON')
def showItemJSON(item_id):
    item = session.query(Item).get(item_id)
    return jsonify(Item=item.serialize)
# end JSON endpoint views


@app.route('/item/<int:item_id>/edit', methods=["POST", "GET"])
def editItem(item_id):
    item = session.query(Item).get(item_id)
    owner = item.user_id
    if 'user_id' in login_session and login_session['user_id'] is owner:
        # If currently logged-in user is owner of item,
        # allow them to edit. This will prevent other
        # users from editing or deleting items they did
        # not submit, even if they manually type the URL
        if request.method == 'POST':
            item.title = request.form['title']
            item.description = request.form['description']
            item.picture = request.form['picture']
            item.genre_id = request.form['genre']
            item.platform_id = request.form['platform']
            session.commit()
            return redirect(url_for('showItem', item_id=item.id))
        else:
            return render_template(
                'editItem.html',
                item=item,
                title="Edit " + item.title,
                genres=GENRES.all(),
                platforms=PLATFORMS.all()
            )
    else:
        # Flash error message and redirect back to item
        flash("You do not have permission to edit this item.")
        return redirect(url_for('showItem', item_id=item.id))


@app.route('/item/<int:item_id>/delete', methods=["POST", "GET"])
def deleteItem(item_id):
    item = session.query(Item).get(item_id)
    owner = item.user_id
    if 'user_id' in login_session and login_session['user_id'] is owner:
        # If currently logged-in user is owner of item,
        # allow them to delete. This will prevent other
        # users from editing or deleting items they did
        # not submit, even if they manually type the URL
        if request.method == 'POST':
            session.delete(item)
            session.commit()
            return redirect(url_for('index'))
        else:
            return render_template(
                'deleteItem.html',
                item=item,
                title="Delete " + item.title,
                genres=GENRES.all(),
                platforms=PLATFORMS.all()
            )
    else:
        # Flash error message and redirect back to item
        flash("You do not have permission to delete this item")
        return redirect(url_for('showItem', item_id=item.id))


@app.route('/genre/<int:genre_id>')
def listByGenre(genre_id):
    # Display all items of defined Genre
    targetGenre = session.query(Genre).get(genre_id)
    items = session.query(Item).filter_by(
        genre_id=genre_id).order_by(Item.title).all()
    return render_template(
        'listItems.html',
        items=items,
        targetGenre=targetGenre,
        title=targetGenre.name,
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
        )


@app.route('/platform/<int:platform_id>')
def listByPlatform(platform_id):
    # Display all items of defined Platform
    targetPlatform = session.query(Platform).get(platform_id)
    items = session.query(Item).filter_by(
        platform_id=platform_id).order_by(Item.title).all()
    return render_template(
        'listItems.html',
        items=items,
        targetPlatform=targetPlatform,
        title=targetPlatform.name,
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
    )


def getUserId(email):
    """Obtains id of User from database.

    Retrieves id of user based on supplied email
    address from user table in database if
    an entry exists.

    Args:
        email: An email address to query database.

    Returns:
        A user id or None, if the user cannot be found.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    """Obtains user object from database.

    Args:
        user_id: A user id to query database.

    Returns:
        A user object with a matching id.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    """Creates a new User object.

    Uses supplied login_session to create a new
    User object and add it to the database.

    Args:
        login_session: A login_session object.

    Returs:
        The id of the newly-created user.
    """
    newUser = User(
        username=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'],
        role_id=3
    )
    session.add(newUser)
    session.commit()
    # Query for newly-created user to return id
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id
