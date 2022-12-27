from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, LoginManager, logout_user, current_user,login_user
from flask_bcrypt import Bcrypt
from forms import RegisterForm, LoginForm, GameForm
from query import get_dashboard_data, get_target
from dataprocessing import iq_list_to_string, iq_string_to_list, pak_list_to_string, pak_string_to_list
from debug import print_game, print_user
import random


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "serializethislater"
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#Database model creation
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    games_in = db.Column(db.String)
    invite_queue = db.Column(db.String)
    loaded_game_id = db.Column(db.Integer)
    def __repr__(self):
        return "<Username %r" % self.id

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    owner = db.Column(db.String(40), nullable=False)
    players_and_kills = db.Column(db.String)
    description = db.Column(db.String)
    is_active = db.Column(db.Boolean, nullable=False)
    join_history = db.Column(db.String(40))
    def __repr__(self):
        return "<Name %r" % self.id
        

with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

#Presents a form for a user to register for an account and inserts data into the database
@app.route('/register', methods=["GET","POST"])
def register(): 
    form = RegisterForm()
    errorMessage = ""
    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            if form.validate_username_email(form.username, form.email, User):
                hashed_password = bcrypt.generate_password_hash(password=form.password.data)
                new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, games_in="", invite_queue="")
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                errorMessage = "Either username already exists or that email is already associated with an account"
        else:
            errorMessage = "Passwords do not match"
    return render_template("register.html", form=form, errorMessage=errorMessage)

#Compares inputted data to database data and gives user access to the service
@app.route('/login', methods=["GET", "POST"])
def login():
    form1 = LoginForm()
    errorMessage = ""
    if form1.validate_on_submit():
        user = User.query.filter_by(email=form1.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form1.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            errorMessage = "Email or password is incorrect"
    return render_template('login.html',form1=form1,errorMessage=errorMessage)

#This is the main body of the application which presents frontend based on the user's interaction with the database
@app.route("/dashboard", methods=["GET","POST"])
@login_required
def dashboard():
    make_game = GameForm()
    #Handles making a game... might change location later
    if make_game.validate_on_submit():
        game = Game.query.filter_by(owner=current_user.username,name=make_game.name.data).first()
        if game:
            return redirect(url_for("dashboard"))
        else:
            new_game = Game(name=make_game.name.data, owner=current_user.username, players_and_kills="0,"+current_user.username+",True", 
            description=make_game.description.data, is_active=False, join_history=str(current_user.id))
            db.session.add(new_game)
            db.session.commit()
            games_in_list = iq_string_to_list(current_user.games_in)
            games_in_list.append(str(new_game.id))
            current_user.games_in = iq_list_to_string(games_in_list)
            current_user.loaded_game_id = new_game.id
            db.session.commit()
            return redirect(url_for("dashboard"))
    #Get all game data for frontend
    user_owned_games,user_invited_games,other_games,loaded_game,leaderboard,target,in_game = get_dashboard_data(Game,current_user)
    leaderboard.sort(reverse=True)
    return render_template("dashboard.html", current_user=current_user, 
    make_game=make_game, user_owned_games_package=[user_owned_games, len(user_owned_games)],
    user_invite_package=[user_invited_games, len(user_invited_games)],
    other_games_package=[other_games,len(other_games)], loaded_game=loaded_game, 
    leaderboard_package=[leaderboard, len(leaderboard)], target=target,
    in_game=in_game)

#When the user switches between games this route handles the database change
@app.route("/switch", methods=["GET","POST"])
@login_required
def switch():
    user = User.query.filter_by(username=current_user.username).first()
    game = Game.query.filter_by(id=request.form["button"]).first()
    user.loaded_game_id = game.id
    db.session.commit()
    return redirect(url_for("dashboard"))

#If the user is the owner of a game, they can invite players to that game which will direct them here
@app.route("/invite", methods=["GET","POST"])
@login_required
def invite():
    loaded_game = Game.query.filter_by(id=current_user.loaded_game_id).first()
    if loaded_game.owner == current_user.username:
        user_to_invite = User.query.filter_by(username = request.form["foreign_username"]).first()
        if user_to_invite and user_to_invite.username != current_user.username:
            loaded_game.players_and_kills += ":0," + request.form["foreign_username"] + ",False"
            if user_to_invite.invite_queue == "":
                user_to_invite.invite_queue += str(loaded_game.id)
            else:
                user_to_invite.invite_queue += "," + str(loaded_game.id)
            db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/leave")
@login_required
def leave():
    curr_game = Game.query.filter_by(id=current_user.id).first()
    player_history = iq_string_to_list(curr_game.join_history)
    player_history.remove(str(current_user.id))
    curr_game.join_history = iq_list_to_string(player_history)
    curr_game_list = iq_string_to_list(current_user.games_in)
    curr_game_list.remove(str(current_user.loaded_game_id))
    if curr_game.owner == current_user.username:
        join_history = iq_string_to_list(curr_game.join_history)
        for i in range(0,len(join_history)):
            user = User.query.filter_by(id=join_history[i]).first()
            in_game_list = iq_string_to_list(user.games_in)
            in_game_list.remove(str(curr_game.id))
            user.games_in = iq_list_to_string(in_game_list)
            if user.loaded_game_id == curr_game.id:
                user.loaded_game_id = None
        db.session.delete(curr_game)
    current_user.games_in = iq_list_to_string(curr_game_list) 
    current_user.loaded_game_id = None
    db.session.commit()
    return redirect(url_for("dashboard"))


#When a user is invited to the game, accepting or declining this invite will be handled here
@app.route("/acceptordecline", methods=["GET","POST"])
@login_required
def accept_or_decline():
    curr_game = Game.query.filter_by(id=list(request.form.values())[0]).first()
    if list(request.form.keys())[0] == "accept":
        games_in_list = iq_string_to_list(current_user.games_in)
        games_in_list.append(list(request.form.values())[0])
        current_user.games_in = iq_list_to_string(games_in_list)
        join_history = iq_string_to_list(curr_game.join_history)
        join_history.append(str(current_user.id))
        curr_game.join_history = iq_list_to_string(join_history)
        user_queue = iq_string_to_list(current_user.invite_queue)
        user_queue.remove(list(request.form.values())[0])
        current_user.invite_queue = iq_list_to_string(user_queue)
        game_players = pak_string_to_list(curr_game.players_and_kills)
        for i in range(0, len(game_players)):
            if game_players[i][1] == current_user.username:
                game_players[i][2] = "True"
                break
        curr_game.players_and_kills = pak_list_to_string(game_players)
        db.session.commit()
    else:
        user_queue = iq_string_to_list(current_user.invite_queue)
        user_queue.remove(list(request.form.values())[0])
        current_user.invite_queue = iq_list_to_string(user_queue)
        game_players = pak_string_to_list(curr_game.players_and_kills)
        for i in range(0, len(game_players)):
            if game_players[i][1] == current_user.username:
                game_players.pop(i)
                break
        curr_game.players_and_kills = pak_list_to_string(game_players)
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/start")
@login_required
def start():
    curr_game = Game.query.filter_by(id=current_user.loaded_game_id).first()
    #Shuffle the players and kills list
    pak_list = pak_string_to_list(curr_game.players_and_kills)
    shuffled_pak_list = []
    for i in range(0,len(pak_list)):
        curr_element = random.choice(pak_list)
        if curr_element[2] == "True":
            shuffled_pak_list.append(curr_element)
        pak_list.remove(curr_element)
    if len(shuffled_pak_list) >= 4:
        curr_game.players_and_kills = pak_list_to_string(shuffled_pak_list)
        #Activate game
        curr_game.is_active = True
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/eliminate")
@login_required
def eliminate():
    curr_game = Game.query.filter_by(id=current_user.loaded_game_id).first()
    target = get_target(curr_game, current_user)
    #Remove the player from the game in the database and from the client game list
    pak_list = pak_string_to_list(curr_game.players_and_kills)
    for i in range(0,len(pak_list)):
        print(pak_list[i][1])
        if pak_list[i][1] == target:
            pak_list.pop(i)
            break
    for i in range(0,len(pak_list)):
        if pak_list[i][1] == current_user.username:
            pak_list[i][0] = str(int(pak_list[i][0]) + 1)
            break
    curr_game.players_and_kills = pak_list_to_string(pak_list)
    db.session.commit()
    return redirect(url_for("dashboard"))

#Logs the user out of the service and returns them to the home screen
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)