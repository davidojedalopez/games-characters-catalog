from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Game, Character, User

engine = create_engine("sqlite:///game_characters_menu.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() isntance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the session
# won't be persisted into the database until you call session.commit().
# If you are not happy about the changes, you can revert all of them back to
# the last commit by calling session.rollback()
session = DBSession()

# Heroes of the Storm Game and Characters
heroes_of_the_storm = Game(name="Heroes of the Storm", 
	logo_url="https://yt3.ggpht.com/-pKiXsuYjEak/AAAAAAAAAAI/AAAAAAAAAAA/h0kGP1NtDr0/s900-c-k-no/photo.jpg")
session.add(heroes_of_the_storm)
session.commit()

raynor = Character(name="Raynor", 
	bio="Ranged Assassin", 
	photo_url="http://www.heroesfire.com/images/skin/raynor-renegade-commander.png", 
	game=heroes_of_the_storm)
session.add(raynor)
session.commit()

leoric = Character(name="Leoric", 
	bio="The Undead King", 
	photo_url="http://cdn.blizzardwatch.com/wp-content/uploads/2015/06/leoric_header.jpg", 
	game=heroes_of_the_storm)
session.add(leoric)
session.commit()

abathur = Character(name="Abathur", 
	bio="Logical Decision", 
	photo_url="http://vignette4.wikia.nocookie.net/starcraft/images/b/b7/Abathur_Heroes_Art1.jpg/revision/latest?cb=20140711045441", 
	game=heroes_of_the_storm)
session.add(abathur)
session.commit()


# Stacraft Game and Characters
starcraft = Game(name="Starcraft", 
	logo_url="http://us.battle.net/sc2/static/images/legacy-of-the-void/header/LotV-header-logo.png")
session.add(starcraft)
session.commit()

artanis = Character(name="Artanis", 
	bio="Protoss hero", 
	photo_url="http://vignette2.wikia.nocookie.net/starcraft/images/c/c9/Artanis_LotV_Art1.jpg/revision/latest?cb=20141108233355", 
	game=starcraft)
session.add(artanis)
session.commit()

nova = Character(name="Nova", 
	bio="Ghost Specialist", 
	photo_url="http://vignette2.wikia.nocookie.net/starcraft/images/5/54/Nova_SC-G_Art2.jpg/revision/latest?cb=20080512071304", 
	game=starcraft)
session.add(nova)
session.commit()

# Overwatch Game and Characters
overwatch = Game(name="Overwatch", 
	logo_url="https://pbs.twimg.com/media/B1-zfpSIEAEnpyw.jpg")
session.add(overwatch)
session.commit()

tracer = Character(name="Tracer", 
	bio="Speddy girl", 
	photo_url="http://hydra-media.cursecdn.com/overwatch.gamepedia.com/thumb/8/81/Tracer-portrait.png/324px-Tracer-portrait.png?version=fa536ff0e224d3bc554c9e31f83805e1", 
	game=overwatch)
session.add(tracer)
session.commit()


print "Added games and characters!"