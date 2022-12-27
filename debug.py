def print_user(User):
    print("id = " + str(User.id))
    print("username = " + User.username)
    print("email = " + User.email)
    print("games_in = " + User.games_in)
    print("invite_queue = " + User.invite_queue)
    print("loaded_game_id = " + str(User.loaded_game_id))
def print_game(Game):
    print("id = " + str(Game.id))
    print("name = " + Game.name)
    print("owner = " + Game.owner)
    print("players_and_kills = " + Game.players_and_kills)
    print("is_active = " + str(Game.is_active))