import os
import csv
import requests
import json
import datetime
import time

from Data.Vars import JOB_MASTER_FILE, JOB_MASTER_HEADERS, CONSTRUCTION_ID, HEALTHCARE_ID
from Util.Auth import refresh_construction_token, refresh_healthcare_token
from Util.Request import make_api_call

''' Project functions '''


def show_projects():
    print("Initializing show_projects()...")

    url = "https://api.procore.com/vapid/projects"
    querystring = {"company_id": CONSTRUCTION_ID}
    headers = {'Authorization': "Bearer " + refresh_construction_token()}
    print("Pulling construction jobs")
    data = json.loads(make_api_call(url, querystring, headers).text)
    projects = data

    print(str(len(data)) + " jobs found")

    querystring = {"company_id": HEALTHCARE_ID}
    headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
    print("Pulling healthcare jobs")
    data = json.loads(make_api_call(url, querystring, headers).text)
    print(str(len(data)) + " jobs found")

    projects += data

    return projects


def get_projects():
    print("Initializing get_projects()...")

    url = "https://api.procore.com/vapid/projects"
    querystring = {"company_id": CONSTRUCTION_ID}
    headers = {'Authorization': "Bearer " + refresh_construction_token()}
    print("Pulling construction jobs")
    data = json.loads(make_api_call(url, querystring, headers).text)
    projects = data

    print(str(len(data)) + " jobs found")

    querystring = {"company_id": HEALTHCARE_ID}
    headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
    print("Pulling healthcare jobs")
    data = json.loads(make_api_call(url, querystring, headers).text)
    print(str(len(data)) + " jobs found")

    projects += data

    write_row(JOB_MASTER_FILE, JOB_MASTER_HEADERS, projects)

    return projects


def write_row(file, headers, data):
    if os.path.isfile(file):
        os.remove(file)

    w = open(file, 'a', newline='', encoding='utf-8')
    w = csv.writer(w)
    w.writerow(headers)

    for i in range(len(data)):
            values = [data[i]['id'], data[i]['project_number'], data[i]['display_name'],
                    data[i]['company']['name'], data[i]['address'], data[i]['city'],
                    data[i]['state_code'], data[i]['country_code'], data[i]['zip'],
                    data[i]['county'], data[i]['latitude'], data[i]['longitude'],
                    data[i]['stage'], data[i]['phone'], data[i]['created_at'],
                    data[i]['updated_at'], data[i]['active'], data[i]['origin_id'],
                    data[i]['origin_data'], data[i]['company']['id'],
                    datetime.datetime.now()]
            w.writerow(values)
get_projects()