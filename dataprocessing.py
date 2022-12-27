

def iq_string_to_list(invite_queue_string):
    if invite_queue_string == "":
        return []
    else:
        return invite_queue_string.split(",")

def iq_list_to_string(invite_queue_list):
    return ",".join(invite_queue_list)


def pak_string_to_list(players_and_kills_string):
    if players_and_kills_string == "":
        return []
    else:
        final_list = []
        first_mod = players_and_kills_string.split(":")
        for i in range(0,len(first_mod)):
            curr_list = first_mod[i].split(",")
            final_list.append(curr_list)
        return final_list

def pak_list_to_string(players_and_kills_list):
    if players_and_kills_list == []:
        return ""
    else:
        first_filter = []
        for i in range(0,len(players_and_kills_list)):
            curr_list = players_and_kills_list[i]
            first_filter.append(",".join(curr_list))
        return ":".join(first_filter)

def get_invited_games(invite_queue, Game):
    if invite_queue == []:
        return []
    else:
        return_list = []
        for i in range(0,len(invite_queue[0])):
            return_list.append(Game.query.filter_by(id=int(invite_queue[0][i])).first())
        return return_list







