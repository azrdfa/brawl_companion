import requests
import time

def get_request(url, headers, data_desc):

    start_time = time.perf_counter()
    print(f"Obtaining {data_desc} ...")

    r = requests.get(url, headers)
    result = None

    if r.status_code == 200:
        result = r.json()
    else:
        if r.status_code == 400:
            print("Client provided incorrect parameters for the request.")
        elif r.status_code == 403:
            print("Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource.")
        elif r.status_code == 404:
            print("Resource was not found.")
        elif r.status_code == 429:
            print("Request was throttled, because amount of requests was above the threshold defined for the used API token.")
        elif r.status_code == 500:
            print("Unknown error happened when handling the request.")
        elif r.status_code == 503:
            print("Service is temprorarily unavailable because of maintenance.")
        exit()

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    print(f"{data_desc} obtained in {round(elapsed_time, 2)} second(s)")

    return result