from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Game, Character, User

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
game1 = Game(name="Heroes of the Storm", logo_url="https://yt3.ggpht.com/-pKiXsuYjEak/AAAAAAAAAAI/AAAAAAAAAAA/h0kGP1NtDr0/s900-c-k-no/photo.jpg")

session.add(game1)
session.commit()

character1 = Character(name="Raynor", bio="Ranged Assassin", photo_url="http://www.heroesfire.com/images/skin/raynor-renegade-commander.png")

session.add(character1)
session.commit()

# Stacraft Game and Characters
game2 = Game(name="Starcraft", logo_url="http://us.battle.net/sc2/static/images/legacy-of-the-void/header/LotV-header-logo.png")

session.add(game2)
session.commit()

character2 = Character(name="Artanis", bio="Protoss hero", photo_url="http://vignette2.wikia.nocookie.net/starcraft/images/c/c9/Artanis_LotV_Art1.jpg/revision/latest?cb=20141108233355")

session.add(character2)
session.commit()

print "Added games and characters!"