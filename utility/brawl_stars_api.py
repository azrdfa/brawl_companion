import concurrent.futures
import threading
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

class MultipleRequest():

    def __init__(self, urls, headers, data_desc):
        # dependent variable
        self.urls = urls
        self.headers = headers
        self.data_desc = data_desc
        # independent variable
        self.success_lock = threading.Lock()
        self.error_lock = threading.Lock()
        self.success_responses = []
        self.error_responses = []
    
    def get_success_responses(self):
        return self.success_responses
    
    def get_error_responses(self):
        return self.error_responses

    def start_requesting(self):

        start_time = time.perf_counter()
        print(f"Obtaining {self.data_desc} ...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.urls)) as executor:
            for url in self.urls:
                executor.submit(self.get_request, url)
        
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        print(f"{self.data_desc} obtained in {round(elapsed_time, 2)} second(s)")

    def get_request(self, url):
        try:
            r = requests.get(url, self.headers)
            result = {
                "player_tag": url.split("/")[-2],
                "status": r.status_code
            }

            if r.status_code == 200:
                result["value"] = r.json()
            else:
                if r.status_code == 400:
                    result["value"] = "Client provided incorrect parameters for the request."
                elif r.status_code == 403:
                    result["value"] = "Access denied, either because of missing/incorrect credentials or used API token does not grant access to the requested resource."
                elif r.status_code == 404:
                    result["value"] = "Resource was not found."
                elif r.status_code == 429:
                    result["value"] = "Request was throttled, because amount of requests was above the threshold defined for the used API token."
                elif r.status_code == 500:
                    result["value"] = "Unknown error happened when handling the request."
                elif r.status_code == 503:
                    result["value"] = "Service is temprorarily unavailable because of maintenance."

            with self.success_lock:
                self.success_responses.append(result)
        except Exception as ex:
            with self.error_lock:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                self.error_responses.append(
                    {"value": message}
                )