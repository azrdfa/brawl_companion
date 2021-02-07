from utility.brawl_stars_api import get_request, MultipleRequest
from utility.brawl_stars_constants import GAME_MODES as gm, GAME_TYPES as gt
from datetime import datetime
from tabulate import tabulate

from dotenv import load_dotenv
load_dotenv()
import os

datetime_format = "%Y-%m-%dT%H:%M:%S"
datetime_obj = datetime.now()
time_stamp_str = datetime_obj.strftime(datetime_format)

headers = {'Authorization': os.environ.get("bearer_token"), 'Content-Type' : 'application/json'}
top_player_url = "https://api.brawlstars.com/v1/rankings/" + os.environ.get("country_code") + "/players"

top_player_response = get_request(top_player_url, headers, "Top Player Data")

battle_log_urls = []
for i in range(len(top_player_response["items"])):
    top_player = top_player_response["items"][i]
    player_tag = "%23" + top_player["tag"][1:]
    battle_log_url = "https://api.brawlstars.com/v1/players/" + player_tag + "/battlelog"
    battle_log_urls.append(battle_log_url)

battle_log_requests = MultipleRequest(battle_log_urls, headers, "Battle Log Data")
battle_log_requests.start_requesting()
battle_log_success_responses = battle_log_requests.get_success_responses()
battle_log_error_responses = battle_log_requests.get_error_responses()

def add_battle_placeholder(battle_mode, battle_map, battle_time, map_dict):
    if battle_mode not in map_dict.keys():
        map_dict[battle_mode] = {}
    if battle_map not in map_dict[battle_mode].keys():
        map_dict[battle_mode][battle_map] = {}
    if battle_time not in map_dict[battle_mode][battle_map].keys():
        map_dict[battle_mode][battle_map][battle_time] = []
    return map_dict

map_dict = {}
battle_log_status_ok, battle_log_status_error = 0 , []
recognized_battle, unrecognized_battle = 0, []
recognized_battle_mode_type, unrecognized_battle_mode_type = 0, []
for battle_log in battle_log_success_responses:
    battle_log_player_tag = battle_log["player_tag"]
    battle_log_status = battle_log["status"]
    if battle_log_status == 200:
        battle_log_status_ok += 1
        for battle in battle_log["value"]["items"]:
            try:
                battle_mode = battle["event"]["mode"]
                battle_map = battle["event"]["map"]
                battle_time = battle["battleTime"]
                battle_type = battle["battle"]["type"]
            except KeyError as ex:
                message = f"Unrecognized battle with KeyError: {ex.args}"
                unrecognized_battle.append(message)
                continue
            else:
                recognized_battle += 1    
            
            if battle_mode in gm and battle_type in gt:
                recognized_battle_mode_type += 1
                battle_record = None
                map_dict = add_battle_placeholder(battle_mode, battle_map, battle_time, map_dict.copy())
                if battle_mode == "hotZone":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                elif battle_mode == "gemGrab":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                elif battle_mode == "soloShowdown":
                    battle_rank = battle["battle"]["rank"]
                    battle_players = battle["battle"]["players"]
                    for player in battle_players:
                        if player["tag"] == battle_log_player_tag:
                            break
                    battle_brawler = player["brawler"]["name"]
                    battle_record = {
                        "rank": battle_rank,
                        "brawler": battle_brawler
                    }
                elif battle_mode == "duoShowdown":
                    battle_rank = battle["battle"]["rank"]
                    battle_teams = battle["battle"]["teams"]
                    for team in battle_teams:
                        team_has_been_found = False
                        for player in team:
                            if player["tag"] == battle_log_player_tag:
                                team_has_been_found = True
                                break
                        if team_has_been_found:
                            break
                    battle_brawler = [player["brawler"]["name"] for player in team]
                    battle_record = {
                        "rank": battle_rank,
                        "brawler": battle_brawler
                    }
                elif battle_mode == "heist":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                elif battle_mode == "bounty":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                elif battle_mode == "brawlBall":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                elif battle_mode == "siege":
                    battle_record = battle["battle"]["starPlayer"]["tag"]
                
                map_dict[battle_mode][battle_map][battle_time].append(
                    battle_record
                )
                
            else:
                message = f"Unrecognized battle mode or type: ({battle_mode}, {battle_type})"
                unrecognized_battle_mode_type.append(message)
    else:
        message = f"{battle_log_player_tag} battle log status error: {battle_log_status}"
        battle_log_status_error.append(message)

print("Last update on", time_stamp_str)

full_error_message = []

print("="*71)
print(f"{len(battle_log_success_responses)} battle log success response")
print(f"{len(battle_log_error_responses)} battle log error response")
full_error_message.append("="*71)
for i in range(len(battle_log_error_responses)):
    full_error_message.append(f"{i+1}. {battle_log_error_responses[i]['value']}")

print("="*71)
print(f"{battle_log_status_ok} battle log status ok")
print(f"{len(battle_log_status_error)} battle log status error")
full_error_message.append("="*71)
for i in range(len(battle_log_status_error)):
    full_error_message.append(f"{i+1}. {battle_log_status_error[i]}")

print("="*71)
print(f"{recognized_battle} recognized battle")
print(f"{len(unrecognized_battle)} unrecognized battle")
full_error_message.append("="*71)
for i in range(len(unrecognized_battle)):
    full_error_message.append(f"{i+1}. {unrecognized_battle[i]}")

print("="*71)
print(f"{recognized_battle_mode_type} recognized battle mode or type")
print(f"{len(unrecognized_battle_mode_type)} unrecognized battle mode or type")
full_error_message.append("="*71)
for i in range(len(unrecognized_battle_mode_type)):
    full_error_message.append(f"{i+1}. {unrecognized_battle_mode_type[i]}")

log_error_filename = "./log/brawler_recommendation_" + time_stamp_str + ".txt"
os.makedirs(os.path.dirname(log_error_filename), exist_ok=True)
with open(log_error_filename, "w") as text_file:
    text_file.write("\n".join(full_error_message))
print(f"Full error message available at {log_error_filename}")