import requests
from dotenv import load_dotenv
from datetime import datetime
import time
from tabulate import tabulate

load_dotenv()
import os

TROPHY_CONDITION = {
    "trophies": [
        (501,524),(525,549),(550,574),(575,599),
        (600,624),(625,649),(650,674),(675,699),
        (700,724),(725,749),(750,574),(775,799),
        (800,824),(825,849),(850,874),(875,899),
        (900,924),(925,949),(950,974),(975,999),
        (1000,1049),(1050,1099),
        (1100,1149),(1150,1199),
        (1200,1249),(1250,1299),
        (1300,1349),(1350,1399),
        (1400,1449),(1450,1499),
        (1500,9999)
    ],
    "star_point_reward": [
        20,50,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350
    ],
    "trophies_after_trophy_league_end": [
        500,524,549,574,599,624,649,674,699,724,749,774,799,824,849,874,885,900,920,940,960,980,1000,1020,1040,1060,1080,1100,1120,1140,1150
    ],
    "total_condition": 31
}

headers = {'Authorization': os.environ.get("bearer_token"), 'Content-Type' : 'application/json'}
url = "https://api.brawlstars.com/v1/players/" + os.environ.get("player_tag")

start_time = time.perf_counter()
print("Obtaining data ...")

r = requests.get(url, headers)
result = None
if r.status_code == 200:
    result = r.json()
elif r.status_code == 403:
    print("Acces Denies !!")
    exit()
else:
    print("Error Occured !!")
    exit()

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Data obtained in {round(elapsed_time, 2)} second(s)")

total_trophies_lost = 0
total_star_point_reward = 0
brawler_trophies_lost = []
datetime_format = "%Y-%m-%dT%H:%M:%S"
datetime_obj = datetime.now()
time_stamp_str = datetime_obj.strftime(datetime_format)
for brawler in result["brawlers"]:
    if brawler["trophies"] > 500:
        for i in range(TROPHY_CONDITION["total_condition"]):
            if brawler["trophies"] >= TROPHY_CONDITION["trophies"][i][0] and brawler["trophies"] <= TROPHY_CONDITION["trophies"][i][1]:
                total_star_point_reward += TROPHY_CONDITION["star_point_reward"][i]
                total_trophies_lost += brawler["trophies"] - TROPHY_CONDITION["trophies_after_trophy_league_end"][i]
                if i == (TROPHY_CONDITION["total_condition"] - 1):
                    brawler_trophies_lost.append((
                        brawler["name"], 
                        brawler["trophies"] - TROPHY_CONDITION["trophies_after_trophy_league_end"][i],
                        brawler["trophies"],
                        "No next checkpoint"
                        ))
                else:
                    brawler_trophies_lost.append((
                        brawler["name"], 
                        brawler["trophies"] - TROPHY_CONDITION["trophies_after_trophy_league_end"][i],
                        brawler["trophies"],
                        TROPHY_CONDITION["trophies"][i+1][0]
                        ))

brawler_trophies_lost.sort(key=lambda x: x[1], reverse = True)

print("="*65)
print("Statistics for", result["name"], "from", time_stamp_str)
print("Current trophies:", result["trophies"])
print("Total trophies lost:", total_trophies_lost)
print("Trophies after trophy league end:", result["trophies"] - total_trophies_lost)
print("Star point reward after trophy league end:", total_star_point_reward)

print("="*65)
print(
    tabulate(brawler_trophies_lost, 
    headers=["Brawler", "Trophies Lost", "Current Trophies", "Next Checkpoint"])
)