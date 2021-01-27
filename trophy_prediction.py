import json
import os
from datetime import datetime

datetime_format = "%Y-%m-%dT%H:%M:%S"
selected_datetime = datetime.strptime("1970-01-01T00:00:00", datetime_format)
for directory in os.listdir("./resources/player_data"):
    datetime_obj = datetime.strptime(directory, datetime_format)
    if datetime_obj > selected_datetime:
        selected_datetime = datetime_obj

contents = []
selected_datetime_str = selected_datetime.strftime(datetime_format)
for filename in os.listdir("./resources/player_data/" + selected_datetime_str):
    file_source = open("./resources/player_data/" + selected_datetime_str + "/" + filename)
    content_json = file_source.read()
    content_dict = json.loads(content_json)
    contents.append(content_dict)

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

for content in contents:
    total_trophies_lost = 0
    total_star_point_reward = 0
    brawler_trophies_lost = []
    for brawler in content["brawlers"]:
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
    print("Statistics for", content["name"], "from", selected_datetime_str)
    print("Current trophies:", content["trophies"])
    print("Total trophies lost:", total_trophies_lost)
    print("Trophies after trophy league end:", content["trophies"] - total_trophies_lost)
    print("Star point reward after trophy league end:", total_star_point_reward)
    for item in brawler_trophies_lost:
        print(f"name: {item[0]}, trophies_lost: {item[1]}, current_trophies: {item[2]}, next checkpoint: {item[3]}")


