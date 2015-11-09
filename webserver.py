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

@app.route("/games/<int:game_id>/")
def showCharacters(game_id):
	game = session.query(Game).filter_by(id=game_id).one
	characters = session.query(Character).filter_by()


if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000)