from dataprocessing import get_invited_games, pak_string_to_list, iq_string_to_list

#methods here are for advanced queries
def get_dashboard_data(Game, current_user):
    user_owned_games = Game.query.filter_by(owner=current_user.username).order_by(Game.name).all()
    user_invited_games = get_invited_games(pak_string_to_list(current_user.invite_queue),Game)
    other_games = []
    games_in_list = iq_string_to_list(current_user.games_in)
    for i in range(0, len(games_in_list)):
        curr_game = Game.query.filter_by(id=games_in_list[i]).first()
        if curr_game.owner != current_user.username:
            other_games.append(curr_game)
    loaded_game = Game.query.filter_by(id=current_user.loaded_game_id).first()
    leaderboard = []
    is_in_game = False
    if loaded_game:
        leaderboard = get_leaderboard(loaded_game)
        is_in_game = in_game(loaded_game,current_user)
    target = get_target(loaded_game, current_user)
    return user_owned_games,user_invited_games,other_games,loaded_game,leaderboard,target,is_in_game

def get_leaderboard(game):
    leaderboard = None
    leaderboard = pak_string_to_list(game.players_and_kills)
    return leaderboard

def get_target(game, current_user):
    if not current_user.loaded_game_id:
        return ""
    pak_list = pak_string_to_list(game.players_and_kills)
    if pak_list == []:
        return ""
    for i in range(0,len(pak_list)):
        if pak_list[i][1] == current_user.username:
            if i == (len(pak_list) - 1):
                return pak_list[0][1]
            else:
                return pak_list[i+1][1]

def in_game(game, current_user):
    game_list = pak_string_to_list(game.players_and_kills)
    for i in range(0,len(game_list)):
        if game_list[i][1] == current_user.username:
            return True
    return False