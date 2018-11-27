import os
import csv
import json

from Util.Auth import refresh_construction_token, refresh_healthcare_token
from Util.Request import make_api_call
from Data.Vars import DAILYLOG_MASTER_FILE, DAILYLOG_JSON_FILE, DAILYLOG_MASTER_HEADERS, CONSTRUCTION_ID, HEALTHCARE_ID
from Build.Projects import show_projects

''' Global Variables '''

HEADERS_WRITTEN = False

''' Project functions '''


def get_dailylog(projects):
    if os.path.isfile(DAILYLOG_JSON_FILE):
        os.remove(DAILYLOG_JSON_FILE)
    output = open(DAILYLOG_JSON_FILE, 'a')

    if os.path.isfile(DAILYLOG_MASTER_FILE):
        os.remove(DAILYLOG_MASTER_FILE)

    print("\n-------------------------------------"
          "\nInitializing get_dailylog_list()")

    for i in range(len(projects)):
        job_index = projects[i]['id']
        job = projects[i]['project_number']
        url = "https://api.procore.com/vapid/projects/" + str(job_index) + "/manpower_logs"

        if isinstance(projects[i]['project_number'], str) and len(projects[i]['project_number']) == 6:
            if projects[i]['company']['id'] == CONSTRUCTION_ID:
                querystring = {"company_id": CONSTRUCTION_ID, "project_id": job_index, "start_date": '2018-11-26',
                               "end_date": "2018-11-27"}
                headers = {'Authorization': "Bearer " + refresh_construction_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " daily logs found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Daily Log " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
            else:
                querystring = {"company_id": HEALTHCARE_ID, "project_id": job_index, "start_date": '2018-11-26',
                               "end_date": "2018-11-27"}
                headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " daily logs found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Daily Log " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
        else:
            continue


def write_row(data, job_index):
    w = open(DAILYLOG_MASTER_FILE, 'a', newline='', encoding='utf-8')
    w = csv.writer(w)

    global HEADERS_WRITTEN
    if HEADERS_WRITTEN == False:
        w.writerow(DAILYLOG_MASTER_HEADERS)
        HEADERS_WRITTEN = True;

    try:
        values = [job_index,
            data['id'],
            data.get('created_at'),
            data.get('date'),
            data.get('notes'),
            data.get('status'),
            data.get('num_workers'),
            data.get('num_hours'),
            data.get('man_hours'),
            '' if isinstance(data['contact'], type(None)) else data['contact']['name'],
            '' if isinstance(data['contact'], type(None)) else data['contact']['email'],
            '' if isinstance(data['contact'], type(None)) else data['contact']['job_title'],
            '' if isinstance(data['contact'], type(None)) else data['contact']['business_phone'],
            '' if isinstance(data['contact'], type(None)) else data['contact']['business_phone_extension'],
            '' if isinstance(data['trade'], type(None)) else data['trade']['name'],
            data.get('created_by').get('name')]
        w.writerow(values)
    except UnicodeEncodeError:
        values = [job_index,
                  data['id'],
                  data.get('created_at'),
                  data.get('date'),
                  data.get('notes'),
                  data.get('status'),
                  data.get('num_workers'),
                  data.get('num_hours'),
                  data.get('man_hours'),
                  '' if isinstance(data['contact'], type(None)) else data['contact']['name'],
                  '' if isinstance(data['contact'], type(None)) else data['contact']['email'],
                  '' if isinstance(data['contact'], type(None)) else data['contact']['job_title'],
                  '' if isinstance(data['contact'], type(None)) else data['contact']['business_phone'],
                  '' if isinstance(data['contact'], type(None)) else data['contact']['business_phone_extension'],
                  '' if isinstance(data['trade'], type(None)) else data['trade']['name'],
                  data.get('created_by').get('name')]
        w.writerow(values)

get_dailylog(show_projects())