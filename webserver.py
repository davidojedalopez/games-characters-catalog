import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Game, Character, User
from flask import session as login_session
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from auth import OAuthSignIn, GoogleSignIn

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.from_pyfile("config.cfg")

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

@app.route("/games/JSON")
def gamesJSON():
	games = session.query(Game).all()
	return jsonify(games=[r.serialize for r in games])

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

@app.route("/games/characters/JSON")
def charactersJSON():
	characters = session.query(Character).all()
	return jsonify(characters=[r.serialize for r in characters])

@app.route("/games/<game_name>/characters/JSON")
def gameCharactersJSON(game_name):
	game = session.query(Game).filter_by(name=game_name).one()
	characters = session.query(Character).filter_by(game=game).all()
	return jsonify(characters=[r.serialize for r in characters])

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

@app.route("/games/<game_name>/delete/", methods=["GET", "POST"])
def deleteGame(game_name):
	gameToDelete = session.query(Game).filter_by(name=game_name).one()
	if request.method == "POST":
		session.delete(gameToDelete)
		flash('%s Successfully Deleted' % gameToDelete.name)
		session.commit()
		return redirect(url_for("showGames"))
	else:
		return render_template("deleteGame.html", game=gameToDelete)

#@app.route("/characters/<character_name>/edit", methods=["GET", "POST"])
@app.route("/games/<game_name>/characters/<character_name>/edit", methods=["GET", "POST"])
def editCharacter(character_name, game_name):
	editedCharacter = session.query(Character).filter_by(name=character_name).one()	
	games = session.query(Game).all()	
	if request.method == "POST":
		game = session.query(Game).filter_by(name=request.form["game"]).one()
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
def deleteCharacter(character_name, game_name):
	characterToDelete = session.query(Character).filter_by(name=character_name).one()
	# Require game instance to avoid "Parent instance is not bound to a Session" error.
	# Not being used for anything more.
	game = session.query(Game).filter_by(name=game_name).one()
	if request.method == "POST":
		session.delete(characterToDelete)
		flash("%s Successfully Deleted" % characterToDelete.name)
		session.commit()
		return redirect(url_for("showCharacters", game_name=characterToDelete.game.name))
	else:
		return render_template("deleteCharacter.html", character=characterToDelete)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('showGames'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('showGames'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('showGames'))
    # Look if the user already exists
    user=session.query(User).filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you 
        # require that.
        user=User(nickname=nickname, email=email)
        session.add(user)
        session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('showGames'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated():
     #   return redirect(url_for('showGames'))
    return render_template('login.html',
                           title='Sign In')

#@app.route("games/<game_name>/characters/<character_name>/delete", methods=["GET", "POST"])
#def deleteCharacter():
if __name__ == "__main__":
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host="0.0.0.0", port=5000)