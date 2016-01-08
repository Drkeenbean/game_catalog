from app import app
from flask import render_template, url_for, request, redirect, jsonify
from flask import session as login_session
from models import Base, Item, Genre, Platform
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import random
import string

engine = create_engine('sqlite:///game_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Constants to store genres and platforms
# for use in navigation menus
GENRES = session.query(Genre).order_by(Genre.name)
PLATFORMS = session.query(Platform).order_by(Platform.name)


@app.route('/')
def index():
    # Get most recent items from the database
    # to display on front page
    recentItems = session.query(Item).order_by(desc(Item.id)).limit(5)
    if login_session:
        return render_template(
            'index.html',
            items=recentItems,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )
    else:
        return render_template(
            'indexPublic.html',
            items=recentItems,
            genres=GENRES.all(),
            platforms=PLATFORMS.all()
        )


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
    return render_template(
        'login.html',
        state=login_session['state'],
        title="Login",
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
    )


@app.route('/item/new', methods=["POST", "GET"])
def newItem():
    if login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        newItem = Item(
            title=request.form['title'],
            description=request.form['description'],
            picture=request.form['picture'],
            genre_id=request.form['genre'],
            platform_id=request.form['platform'],
            user_id=1
        )
        session.add(newItem)
        session.commit()
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
    return render_template(
        'item.html',
        item=item,
        title=item.title,
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
    )


@app.route('/recents_JSON')
def showRecentJSON():
    recentItems = session.query(Item).order_by(desc(Item.id)).limit(5)
    return jsonify(RecentItems=[i.serialize for i in recentItems])


@app.route('/allItems_JSON')
def showAllJSON():
    allItems = session.query(Item).order_by(Item.id).all()
    return jsonify(AllItems=[i.serialize for i in allItems])


@app.route('/item/<int:item_id>_JSON')
def showItemJSON(item_id):
    item = session.query(Item).get(item_id)
    return jsonify(Item=item.serialize)


@app.route('/item/<int:item_id>/edit', methods=["POST", "GET"])
def editItem(item_id):
    item = session.query(Item).get(item_id)
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


@app.route('/item/<int:item_id>/delete', methods=["POST", "GET"])
def deleteItem(item_id):
    item = session.query(Item).get(item_id)
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


@app.route('/genre/<int:genre_id>')
def listByGenre(genre_id):
    targetGenre = session.query(Genre).get(genre_id)
    items = session.query(Item).filter_by(genre_id=genre_id).order_by(Item.title).all()
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
    targetPlatform = session.query(Platform).get(platform_id)
    items = session.query(Item).filter_by(platform_id=platform_id).order_by(Item.title).all()
    return render_template(
        'listItems.html',
        items=items,
        targetPlatform=targetPlatform,
        title=targetPlatform.name,
        genres=GENRES.all(),
        platforms=PLATFORMS.all()
    )

# TODO: Add views for users
