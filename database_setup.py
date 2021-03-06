from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask.ext.login import LoginManager, UserMixin

Base = declarative_base()


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, Sequence("game_id_seq"), primary_key=True)
    name = Column(String(50), nullable=False)
    logo_url = Column(String(250), nullable=False)


class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, Sequence("character_id_seq"), primary_key=True)
    name = Column(String(30), nullable=False)
    bio = Column(String(400))
    photo_url = Column(String(250), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"))
    game = relationship(Game)


class User(UserMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    # social_id: Unique identifier from the third party auth service
    social_id = Column(String(50), nullable=False, unique=True)
    nickname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

engine = create_engine("sqlite:///game_characters_menu.db")

Base.metadata.create_all(engine)
