import os
from flask import Flask, render_template, request, redirect, url_for, flash
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
def redirectToGames():
	return redirect("/games/")

@app.route("/games/")
def showGames():
	games = session.query(Game)
	return render_template("games.html", games=games)

@app.route("/characters/")
def showAllCharacters():
	characters = session.query(Character).all()
	return render_template("characters.html", characters=characters)

@app.route("/games/<game_name>/")
def redirectToCharacters(game_name):
	return redirect("games/%s/characters" % game_name)

@app.route("/games/<game_name>/characters")
def showCharacters(game_name):
	game = session.query(Game).filter_by(name=game_name).one()
	characters = session.query(Character).filter_by(game_id=game.id).all()
	return render_template("characters.html", characters=characters, game=game)

@app.route("/games/new/", methods=["GET", "POST"])
def newGame():
    if request.method == "POST":
        newGame = Game(name=request.form["name"], logo_url=request.form["logo_url"])
        session.add(newGame)
        flash("New Game %s Successfully Created" % newGame.name)
        session.commit()
        return redirect(url_for("showGames"))
    else:
        return render_template("newGame.html")

@app.route("/characters/new", methods=["GET", "POST"])
def newCharacter():
	if request.method == "POST":
		game = session.query(Game).filter_by(name=request.form["game"]).one()
		newCharacter = Character(name=request.form["name"], game=game, photo_url=request.form["photo_url"])
		session.add(newCharacter)
		flash("New Character %s Successfully Created" % newCharacter.name)
		session.commit()
		return redirect(url_for("showAllCharacters"))
	else:
		return render_template("newCharacter.html")

@app.route("/games/<game_name>/edit/", methods=["GET", "POST"])
def editGame(game_name):
	editedGame = session.query(Game).filter_by(name=game_name).one()
	if request.method == "POST":
		if request.form["name"] and request.form["logo_url"]:
			editedGame.name = request.form["name"]
        	flash("Game Successfully Edited %s" % editedGame.name)
        	editedGame.logo_url = request.form["logo_url"]
        	flash("Game Successfully Edited %s" % editedGame.logo_url)
        	return redirect(url_for("showGames"))
	else:
		return render_template("editGame.html", game=editedGame)

#@app.route("/characters/<character_name>/edit", methods=["GET", "POST"])
@app.route("/games/<game_name>/characters/<character_name>/edit", methods=["GET", "POST"])
def editCharacter(character_name, game_name):
	editedCharacter = session.query(Character).filter_by(name=character_name).one()
	game = session.query(Game).filter_by(name=editedCharacter.game.name).one()
	if request.method == "POST":
		if request.form["name"] and request.form["photo_url"] and request.form["game"]:
			editedCharacter.name = request.form["name"]
			flash("Character Successfully Edited %s" % editedCharacter.name)
			editedCharacter.photo_url = request.form["photo_url"]
			flash("Character Successfully Edited %s" % editedCharacter.photo_url)			
			editedCharacter.game = game
			flash("Character Successfully Edited %s" % editedCharacter.game)
			return redirect(url_for("showCharacters", game_name=game.name))
	else:
		return render_template("editCharacter.html", character=editedCharacter, game=game)


if __name__ == "__main__":
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host="0.0.0.0", port=5000)