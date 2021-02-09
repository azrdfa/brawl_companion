from function.calculate_trophy_league_stat import calculate_trophy_league_stat
from utility.constants import TROPHY_CONDITIONS
from utility.api import get_request
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

tt = result["trophies"] # total_trophy
tls = calculate_trophy_league_stat(result, TROPHY_CONDITIONS) # trophy league stat
ttl = tls[0] # total_trophy_lost
tspr = tls[1] # total_star_point_reward
btl = tls[2] # brawler_trophy_lost

print("Last update on", time_stamp_str)

print("="*40)
print("Total trophy:", tt)
print("Total trophy lost:", ttl)
print("Total trophy reset:", tt - ttl)
print("Total star point reward:", tspr)

print("="*40)
print(
    tabulate(btl, 
    headers=["No", "Brawler", "Trophy", "Trophy Lost"])
)