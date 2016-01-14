from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    picture = Column(String(250))
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    role = relationship(Role)

    def __repr__(self):
        return self.username

    @property
    def serialize(self):
        return {
            'username':     self.username,
            'email':        self.email,
            'picture':      self.picture
        }


class Platform(Base):
    __tablename__ = 'platform'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(Text)
    picture = Column(String(250))
    platform_id = Column(Integer, ForeignKey('platform.id'))
    platform = relationship(Platform)
    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    def __repr__(self):
        return self.title

    @property
    def serialize(self):
        return {
            'id':           self.id,
            'title':        self.title,
            'description':  self.description,
            'platform':     self.platform.name,
            'genre':        self.genre.name,
            'user':         self.user.username
        }

engine = create_engine('postgresql:///game_catalog')
Base.metadata.create_all(engine)
