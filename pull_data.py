import requests
from dotenv import load_dotenv
from datetime import datetime
import time
import concurrent.futures

load_dotenv()
import os

players_tag = ["%232R8P0PVUJ","%238GRC9U99"]
bearer_token = os.environ.get("bearer_token")
headers = {'Authorization': bearer_token, 'Content-Type' : 'application/json'}

def get_player_info(url, headers):
    return requests.get(url, headers=headers)

start_time = time.perf_counter()

result_dict = {}
with concurrent.futures.ThreadPoolExecutor() as executor:
    for player in players_tag:
        url = "https://api.brawlstars.com/v1/players/" + player
        result = executor.submit(get_player_info, url, headers)
        result_dict[player] = result

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"{len(result_dict)} data obtained in {round(elapsed_time, 2)} second(s)")

# helper
for key in result_dict:
    result_dict[key] = result_dict[key].result()

datetime_format = "%Y-%m-%dT%H:%M:%S"
datetime_obj = datetime.now()
time_stamp_str = datetime_obj.strftime(datetime_format)

for key in result_dict:
    filename = "./resources/player_data/" + time_stamp_str + "/" + key + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as text_file:
        text_file.write(result_dict[key].text)