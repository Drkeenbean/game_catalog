from models import Base, Role, User, Genre, Platform, Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql:///game_catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create 3 basic user roles
newRole = Role(
    name="Administrator",
    description="User with full control of the site"
)
session.add(newRole)

newRole = Role(
    name="Editor",
    description="User with edit permissions to items"
)
session.add(newRole)

newRole = Role(
    name="Contributor",
    description="Basic user. Can add items and edit own items")
session.add(newRole)

# Create admin user
newUser = User(
    username="Admin",
    email="admin@site.com",
    picture="/static/img/1.png",
    role_id=1
)
session.add(newUser)

# Create demo genres and platforms
newGenre = Genre(name="Action")
session.add(newGenre)
newGenre = Genre(name="Adventure")
session.add(newGenre)
newGenre = Genre(name="RPG")
session.add(newGenre)
newGenre = Genre(name="MMO")
session.add(newGenre)
newGenre = Genre(name="Strategy")
session.add(newGenre)
newGenre = Genre(name="Shooter")
session.add(newGenre)

newPlatform = Platform(name="PC")
session.add(newPlatform)
newPlatform = Platform(name="Playstation 4")
session.add(newPlatform)
newPlatform = Platform(name="Playstation 3")
session.add(newPlatform)
newPlatform = Platform(name="Xbox 360")
session.add(newPlatform)
newPlatform = Platform(name="Xbox One")
session.add(newPlatform)
newPlatform = Platform(name="Wii U")
session.add(newPlatform)

# Create a demo item
newItem = Item(
    title="Destiny",
    description="An online shooter from the makers of Halo.",
    picture="https://upload.wikimedia.org/\
    wikipedia/en/thumb/b/be/Destiny_box_art.png/250px-Destiny_box_art.png",
    genre_id=1,
    platform_id=2,
    user_id=1
)
session.add(newItem)

session.commit()
