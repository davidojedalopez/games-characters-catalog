from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Game(Base):
	__tablename__ = "game"

	id = Column(Integer, Sequence("game_id_seq"), primary_key=True)
	name = Column(String(50), nullable=False)	
	logo_url = Column(String(250), nullable=False)

	@property
	def serialize(self):
		"""Return object data in an easily serializable format"""
		return {
			"id" : self.id,
			"name" : self.name,
			"logo_url" : self.logo_url
		}

class Character(Base):
	__tablename__ = "character"

	id = Column(Integer, Sequence("character_id_seq"), primary_key=True)
	name = Column(String(30), nullable=False)
	bio = Column(String(250))
	photo_url = Column(String(250), nullable=False)
	game_id = Column(Integer, ForeignKey("game.id"))
	game = relationship(Game, cascade="all")

	@property
	def serialize(self):
		"""Return object data in an easily serializable format"""
		return {
			"id" : self.id,
			"name" : self.name,
			"bio" : self.bio,
			"photo_url" : self.photo_url,
		}

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
	email = Column(String(50), nullable=False)
	profile_photo_url = Column(String(250))

	@property
	def serialize(self):
		"""Return object data in an easily serializable format"""
		return {
			"id" : self.id,
			"email" : self.email,
			"profile_photo_url" : self.profile_photo_url,
		}

engine = create_engine("sqlite:///game_characters_menu.db")

Base.metadata.create_all(engine)