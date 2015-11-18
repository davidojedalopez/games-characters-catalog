import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Game, Character, User
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from oauth import OAuthSignIn
from lxml import etree

app = Flask(__name__)
# Create a Login Manager instance for the log in and log out of users
login_manager = LoginManager(app)

# Base configuration. Probably better on an external file?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_characters_menu.d'
app.config['OAUTH_CREDENTIALS'] = {
	'facebook': {
		'id': '470154729788964',
		'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
	},
	'google': {
		'id': '329604591768-jeq2ugfhdfm6r6324arcckmdamdr5g36.apps.googleusercontent.com',
		'secret': 'tWckctJkAaUY4x-8Tedjc1c7'
	}
}

engine = create_engine("sqlite:///game_characters_menu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
def redirectToGames():
	"""
	Redirects to main page, games.
	"""
	return redirect("/games/")

@app.route("/games/")
def showGames():
	"""
	Shows all the available games on the games.html template.
	"""
	# Get all games
	games = session.query(Game)
	return render_template("games.html", games=games)

@app.route("/games/JSON")
def gamesJSON():
	"""
	API endpoint for JSON. Shows all the games with its characters.
	"""
	# Get all games
	games = session.query(Game).all()
	return jsonify(games=[r.serialize for r in games])

@app.route("/games/XML")
def gamesXML():
	"""
	API endpoint for XML. Shows all the games with its characters.
	"""
	# Get all games
	games = session.query(Game).all()

	# Build the XML tree with strings
	xml_response ="<games>"

	for game in games:

		# Get all the characters of the game
		characters = session.query(Character).filter_by(game_id=game.id)	

		xml_response += """
			<game>
				<name>
					{0}
				</name>
				<logo_url>
					{1}
				</logo_url>""".format(game.name, game.logo_url)
		# if there are characters for the game, list them too
		if characters != None:
			xml_response += "<characters>"
			for character in characters:					
				xml_response += """
					<character>					
					<name>{0}</name>
					<bio>{1}</bio>
					<photo_url>{2}</photo_url>
					</character>
					""".format(character.name, character.bio, character.photo_url)
			xml_response += "</characters>"
		xml_response += "</game>"
	xml_response += "</games>"
	return xml_response, 200, {'Content-Type': 'text/xml; charset=utf-8'}

@app.route("/characters/")
def showAllCharacters():
	"""
	Shows all characters.
	"""
	characters = session.query(Character).all()
	return render_template("characters.html", characters=characters)

@app.route("/games/<game_name>/")
def redirectToCharacters(game_name):
	"""
	Redirects to characters page for the specified game.
	"""
	return redirect("games/%s/characters" % game_name)

@app.route("/games/<game_name>/characters")
def showCharacters(game_name):
	"""
	Shows all the characters of the specified game.
	"""
	game = session.query(Game).filter_by(name=game_name).one()
	characters = session.query(Character).filter_by(game_id=game.id).all()
	return render_template("characters.html", characters=characters, game=game)

@app.route("/games/new/", methods=["GET", "POST"])
@login_required
def newGame():
	"""
	Creates a new game.
	"""
	# If the route was accessed with a POST method
	if request.method == "POST":
	# Create game from form values
		newGame = Game(name=request.form["name"], logo_url=request.form["logo_url"])
		session.add(newGame)
		flash("New Game %s Successfully Created" % newGame.name)
		session.commit()
		return redirect(url_for("showGames"))
	else:
		return render_template("newGame.html")

@app.route("/characters/new", methods=["GET", "POST"])
@login_required
def newCharacter():
	"""
	Creates a new character.
	"""
	# If the route was accessed with a POST method
	if request.method == "POST":
		game = session.query(Game).filter_by(name=request.form["game"]).one()
		# Create a character from form values
		newCharacter = Character(name=request.form["name"], game=game, photo_url=request.form["photo_url"])
		session.add(newCharacter)
		flash("New Character %s Successfully Created" % newCharacter.name)
		session.commit()
		return redirect(url_for("showCharacters", game_name=game.name))
	else:
		games = session.query(Game).all()
		return render_template("newCharacter.html", games=games)

@app.route("/games/<game_name>/edit/", methods=["GET", "POST"])
@login_required
def editGame(game_name):
	"""
	Edits the selected game.
	"""
	# Get the game to edit
	editedGame = session.query(Game).filter_by(name=game_name).one()
	# If the route was accessed with a POST method
	if request.method == "POST":
		# Get the new values from the form
		if request.form["name"] and request.form["logo_url"]:
			editedGame.name = request.form["name"]
			flash("Game Successfully Edited %s" % editedGame.name)
			editedGame.logo_url = request.form["logo_url"]
			flash("Game Successfully Edited %s" % editedGame.logo_url)
			return redirect(url_for("showGames"))
	else:
		return render_template("editGame.html", game=editedGame)

@app.route("/games/<game_name>/delete/", methods=["GET", "POST"])
@login_required
def deleteGame(game_name):
	"""
	Deletes the specified game.
	"""
	# Select the game to delete
	gameToDelete = session.query(Game).filter_by(name=game_name).one()
	# If the route was accessed with a POST method
	if request.method == "POST":
		session.delete(gameToDelete)
		flash('%s Successfully Deleted' % gameToDelete.name)
		session.commit()
		return redirect(url_for("showGames"))
	else:
		return render_template("deleteGame.html", game=gameToDelete)

@app.route("/games/<game_name>/characters/<character_name>/edit", methods=["GET", "POST"])
@login_required
def editCharacter(character_name, game_name):
	"""
	Edits a character.
	"""
	# Get the character to edit
	editedCharacter = session.query(Character).filter_by(name=character_name).one()	
	games = session.query(Game).all()
	# If the route was accessed with a POST method
	if request.method == "POST":
		game = session.query(Game).filter_by(name=request.form["game"]).one()
		# If all the requested values are filled
		if request.form["name"] and request.form["photo_url"] and game:						
			editedCharacter.name = request.form["name"]			
			flash("Character Successfully Edited %s" % editedCharacter.name)
			editedCharacter.photo_url = request.form["photo_url"]
			flash("Character Successfully Edited %s" % editedCharacter.photo_url)			
			editedCharacter.game = game			
			flash("Character Successfully Edited %s" % editedCharacter.game)			
			return redirect(url_for("showCharacters", game_name=game.name))
	else:
		return render_template("editCharacter.html", character=editedCharacter, games=games)

@app.route("/games/<game_name>/characters/<character_name>/delete", methods=["GET", "POST"])
@login_required
def deleteCharacter(character_name, game_name):
	"""
	Deletes a character.
	"""
	# Selects the character to delete
	characterToDelete = session.query(Character).filter_by(name=character_name).one()
	# Require game instance to avoid "Parent instance is not bound to a Session" error.
	# Not being used for anything more.
	game = session.query(Game).filter_by(name=game_name).one()
	# If the route was accessed with a POST method
	if request.method == "POST":
		session.delete(characterToDelete)
		flash("%s Successfully Deleted" % characterToDelete.name)
		session.commit()
		return redirect(url_for("showCharacters", game_name=characterToDelete.game.name))
	else:
		return render_template("deleteCharacter.html", character=characterToDelete)

@login_manager.user_loader
def load_user(id):
	"""
	Loads user information based on ID.
	"""
	return session.query(User).get(int(id))

@app.route('/logout')
@login_required
def logout():
	"""
	Logs out the current logged in user.
	"""
	logout_user()
	return redirect(url_for('showGames'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	"""
	Creates the OAuthSignIn instance with the given provider, then continues the authorization flow.
	"""
	if not current_user.is_anonymous:
		return redirect(url_for('showGames'))
	oauth = OAuthSignIn.get_provider(provider)
	return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
	"""
	Callback function for OAuth flow.
	"""
	if not current_user.is_anonymous:
		return redirect(url_for('showGames'))
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email = oauth.callback()
	if social_id is None:
		flash('Authentication failed.')
		return redirect(url_for('showGames'))
	user = session.query(User).filter_by(social_id=social_id).first()
	if not user:
		user = User(social_id=social_id, nickname=username, email=email)
		session.add(user)
		session.commit()
	login_user(user, True)
	return redirect(url_for('showGames'))

if __name__ == "__main__":
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host="0.0.0.0", port=5000)