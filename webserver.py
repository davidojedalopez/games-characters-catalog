from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Game, Character
from flask import session as login_session

app = Flask(__name__)

engine = create_engine("sqlite:///game_characters_menu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/games/")
def showGames():
	games = session.query(Game)
	return render_template("games.html", games=games)

@app.route("/characters/")
def showAllCharacters():
	characters = session.query(Character).all()
	return render_template("characters.html", characters=characters)

@app.route("/games/<game_name>/")
@app.route("/games/<game_name>/characters")
def showCharacters(game_name):
	game = session.query(Game).filter_by(name=game_name).one()
	characters = session.query(Character).filter_by(game_id=game.id).all()
	return render_template("characters.html", characters=characters, game=game)


if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000)