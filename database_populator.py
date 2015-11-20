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

leoric = Character(name="Leoric", 
	bio="Leoric, The Skeleton King, is a melee warrior hero from the Blizzard Entertainment Diablo franchise.\
	Madness. Betrayal. Death. These are the legacy of the Black King Leoric's reign. Driven to madness by the \
	spirit of Diablo, Leoric brought untold suffering on his kingdom. Even after his death there was no release\
	for the Skeleton King.", 
	photo_url="http://cdn.blizzardwatch.com/wp-content/uploads/2015/06/leoric_header.jpg", 
	game=heroes_of_the_storm)
session.add(leoric)
session.commit()

abathur = Character(name="Abathur", 
	bio="Abathur, the Evolution Master, is a melee specialist hero from the Blizzard Entertainment StarCraft franchise. \
	Abathur, the Evolution Master of Kerrigan's Swarm, works ceaselessly to improve the zerg from the genetic level up. \
	Abathur does not directly engage in combat, but rather can act through his allied Heroes and Minions and place Toxic \
	Nests to defend important locations.",
	photo_url="http://vignette4.wikia.nocookie.net/starcraft/images/b/b7/Abathur_Heroes_Art1.jpg/revision/latest?cb=20140711045441",
	game=heroes_of_the_storm)
session.add(abathur)
session.commit()

nova = Character(name="Nova", 
	bio="November 'Nova' Terra, the Dominion Ghost, is a ranged assassin hero from the Blizzard Entertainment StarCraft franchise. \
	She is a ghost of the Terran Dominion and one of the most powerful psionic soldiers ever known. Nova is highly focused, \
	determined, and extremely deadly. Even Jim Raynor wouldn't want to be caught within her crosshairs", 
	photo_url="http://vignette2.wikia.nocookie.net/starcraft/images/5/54/Nova_SC-G_Art2.jpg/revision/latest?cb=20080512071304", 
	game=heroes_of_the_storm)
session.add(nova)
session.commit()

# Stacraft Game and Characters
starcraft = Game(name="Starcraft", 
	logo_url="http://screenshots.en.sftcdn.net/en/scrn/304000/304793/starcraft-2-13.png")
session.add(starcraft)
session.commit()

raynor = Character(name="Raynor", 
	bio="Jim Raynor, the Renegade Commander, is a ranged assassin hero from the Blizzard Entertainment StarCraft franchise. \
	The Ex-Confederate Marshall has stood against whatever the universe can throw at him and survived. He stands as a bright \
	beacon of hope among enigmatic aliens and monsters, still fighting for justice in a cold uncaring universe.", 
	photo_url="http://www.heroesfire.com/images/skin/raynor-renegade-commander.png", 
	game=starcraft)
session.add(raynor)
session.commit()

artanis = Character(name="Artanis", 
	bio="Artanis is the leader of the Daelaam. A renowned warrior, he seeks to unify his beleaguered people, and will let \
	nothing stand in his way to restore the glory of the protoss.", 
	photo_url="http://vignette2.wikia.nocookie.net/starcraft/images/c/c9/Artanis_LotV_Art1.jpg/revision/latest?cb=20141108233355", 
	game=starcraft)
session.add(artanis)
session.commit()

# Overwatch Game and Characters
overwatch = Game(name="Overwatch", 
	logo_url="http://i.imgur.com/YZ4w2ey.png")
session.add(overwatch)
session.commit()

tracer = Character(name="Tracer", 
	bio="With a unique ability to control the speed of her own passage through time, Tracer zips and blinks around the battlefield,\
	 eluding attackers and sneaking past defenses. A perfect skirmisher hero, Tracer is fragile but hard to hit, keeping one step \
	 ahead of her attackers while she harasses and harries the enemy team.", 
	photo_url="http://hydra-media.cursecdn.com/overwatch.gamepedia.com/thumb/8/81/Tracer-portrait.png/324px-Tracer-portrait.png?version=fa536ff0e224d3bc554c9e31f83805e1", 
	game=overwatch)
session.add(tracer)
session.commit()

# Zelda Game and Characters
zelda = Game(name="Zelda",
	logo_url="http://www.cliparthut.com/clip-arts/369/legend-of-zelda-triforce-logo-369837.png")
session.add(zelda)
session.commit()

# Super Smash Bros Game and Characters
super_smash = Game(name="Super Smash Bros.",
	logo_url="http://orig04.deviantart.net/9b0f/f/2014/341/f/1/ssb_symbol_by_britishvideogamenerd-d8905u7.png")
session.add(super_smash)
session.commit()

# Gears of War Game and Characters
gears_of_war = Game(name="Gears of War",
	logo_url="http://orig05.deviantart.net/e71d/f/2008/143/d/5/gears_of_war_2_logo_by_ironno0b.jpg")
session.add(gears_of_war)
session.commit()

print "Added games and characters!"