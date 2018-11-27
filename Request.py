import requests
import time


def make_api_call(url, querystring, headers):
    first_delay = 60
    second_delay = 120
    third_delay = 180

    try:
        print("Sending request to " + url)
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        print("Success! " + str(response.headers.get('X-Rate-Limit-Remaining', 1)) + " requests remaining")
    except requests.exceptions.HTTPError:
        try:
            print("[CRITICAL] ConnectionError caught. Sleeping for " + str(first_delay) + " seconds before 2nd attempt.")
            time.sleep(first_delay)
            response = requests.request("GET", url, headers=headers, params=querystring)
            response.raise_for_status()
            print("Success! " + response.headers.get('X-Rate-Limit-Remaining', 1) + " requests remaining")
        except requests.exceptions.HTTPError:
            try:
                print("[CRITICAL] ConnectionError caught. Sleeping for " + str(second_delay) + " seconds before 3rd attempt.")
                time.sleep(second_delay)
                response = requests.request("GET", url, headers=headers, params=querystring)
                response.raise_for_status()
                print("Success! " + response.headers.get('X-Rate-Limit-Remaining', 1) + " requests remaining")
            except requests.exceptions.HTTPError:
                print("[CRITICAL] ConnectionError caught. Sleeping for " + str(third_delay) + " seconds before final attempt.")
                time.sleep(third_delay)
                response = requests.request("GET", url, headers=headers, params=querystring)
                response.raise_for_status()
                print("Success! " + response.headers.get('X-Rate-Limit-Remaining', 1) + " requests remaining")

    return response

