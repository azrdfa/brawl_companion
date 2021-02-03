from utility.brawl_stars_constants import TROPHY_CONDITION as tc
from utility.brawl_stars_api import get_request
from datetime import datetime
from tabulate import tabulate

from dotenv import load_dotenv
load_dotenv()
import os

datetime_format = "%Y-%m-%dT%H:%M:%S"
datetime_obj = datetime.now()
time_stamp_str = datetime_obj.strftime(datetime_format)

headers = {'Authorization': os.environ.get("bearer_token"), 'Content-Type' : 'application/json'}
player_info_url = "https://api.brawlstars.com/v1/players/" + os.environ.get("player_tag")

result = get_request(player_info_url, headers, os.environ.get("player_tag") + " Personal Data")

total_trophies_lost = 0
total_star_point_reward = 0
brawler_trophies_lost = []
for brawler in result["brawlers"]:
    if brawler["trophies"] > 500:
        for i in range(tc["total_condition"]):
            if brawler["trophies"] >= tc["trophies"][i][0] and brawler["trophies"] <= tc["trophies"][i][1]:
                total_star_point_reward += tc["star_point_reward"][i]
                total_trophies_lost += brawler["trophies"] - tc["trophies_after_trophy_league_end"][i]
                brawler_trophies_lost_item = [
                    brawler["name"], 
                    brawler["trophies"] - tc["trophies_after_trophy_league_end"][i],
                    brawler["trophies"]
                ]
                if i == (tc["total_condition"] - 1):
                    brawler_trophies_lost_item.append("No next checkpoint")
                else:
                    brawler_trophies_lost_item.append(tc["trophies"][i+1][0])
                brawler_trophies_lost.append(brawler_trophies_lost_item)

brawler_trophies_lost.sort(key=lambda x: x[1], reverse = True)
for i in range(len(brawler_trophies_lost)):
    brawler_trophies_lost[i].insert(0, i+1)

print("Last update on", time_stamp_str)

print("="*71)
print("Total current trophies:", result["trophies"])
print("Total trophies lost:", total_trophies_lost)
print("Total trophies after trophy league end:", result["trophies"] - total_trophies_lost)
print("Star point reward after trophy league end:", total_star_point_reward)

print("="*71)
print(
    tabulate(brawler_trophies_lost, 
    headers=["No", "Brawler", "Trophies Lost", "Current Trophies", "Next Checkpoint"])
)