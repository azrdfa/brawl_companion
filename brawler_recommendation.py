from utility.brawl_stars_api import get_request, MultipleRequest
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

player_tags = []
battle_log_urls = []
for i in range(len(top_player_response["items"])):
    top_player = top_player_response["items"][i]
    player_tag = "%23" + top_player["tag"][1:]
    player_tags.append(player_tag)
    battle_log_url = "https://api.brawlstars.com/v1/players/" + player_tag + "/battlelog"
    battle_log_urls.append(battle_log_url)

battle_log_requests = MultipleRequest(battle_log_urls, headers, "Battle Log Data")
battle_log_requests.start_requesting()
battle_log_responses = battle_log_requests.get_responses()

not_obtained_player_tags = []
obtained_player_tags = [battle_log["player_tag"] for battle_log in battle_log_responses]
for player_tag in player_tags:
    if player_tag not in obtained_player_tags:
        not_obtained_player_tags.append(player_tag)

map_dict = {}
battle_log_success, battle_log_error = 0 , []
battle_success, battle_error = 0, []
for battle_log in battle_log_responses:
    if battle_log["status"] == 200:
        battle_log_success += 1
        battle_log_player_tag = battle_log["player_tag"]
        for battle in battle_log["value"]["items"]:
            try:
                battle_mode = battle["event"]["mode"]
                battle_map = battle["event"]["map"]
                battle_time = battle["battleTime"]
                if battle_mode not in map_dict.keys():
                    map_dict[battle_mode] = {}
                if battle_map not in map_dict[battle_mode].keys():
                    map_dict[battle_mode][battle_map] = {}
                if battle_time not in map_dict[battle_mode][battle_map].keys():
                    map_dict[battle_mode][battle_map][battle_time] = []

                if battle_mode == "soloShowdown":
                    battle_result = battle["battle"]["rank"]
                    battle_brawler = None
                    for player in battle["battle"]["players"]:
                        if player["tag"] == battle_log_player_tag:
                            battle_brawler = player["brawler"]["name"]
                            break
                    map_dict[battle_mode][battle_map][battle_time].append(
                        {"rank": battle_result, "brawler": battle_brawler}
                    )
                elif battle_mode == "duoShowdown":
                    battle_result = battle["battle"]["rank"]
                    for team in battle["battle"]["teams"]:
                        team_has_been_found = False
                        for player in team:
                            if player["tag"] == battle_log_player_tag:
                                team_has_been_found = True
                                break
                        if team_has_been_found:
                            break
                    battle_team = [player["brawler"]["name"] for player in team]
                    map_dict[battle_mode][battle_map][battle_time].append(
                        {"rank": battle_result, "team": battle_team}
                    )
                else:
                    battle_star_player = battle["battle"]["starPlayer"]["tag"]
                    map_dict[battle_mode][battle_map][battle_time].append(
                        battle_star_player
                    )
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                battle_error.append(message)
            else:
                battle_success += 1
    else:
        message = f"{battle_log['player_tag']} obtained battle log error, status_code: {battle_log['status']}"
        battle_log_error.append(message)

print("Last update on", time_stamp_str)

print("="*71)
print(f"{len(battle_log_responses)} request success")
print(f"{len(not_obtained_player_tags)} request error")
for i in range(len(not_obtained_player_tags)):
    print(f"{i+1}. {not_obtained_player_tags[i]} not obtained")

print("="*71)
print(f"{battle_log_success} battle log success")
print(f"{len(battle_log_error)} battle log error")
for i in range(len(battle_log_error)):
    print(f"{i+1}. {battle_log_error[i]}")

print("="*71)
print(f"{battle_success} battle success")
print(f"{len(battle_error)} battle error")
for i in range(len(battle_error)):
    print(f"{i+1}. {battle_error[i]}")
