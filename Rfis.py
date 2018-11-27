import os
import csv
import json

from Data.Vars import RFI_MASTER_FILE, RFI_MASTER_HEADERS, RFI_JSON_FILE, CONSTRUCTION_ID, HEALTHCARE_ID
from Util.Auth import refresh_construction_token, refresh_healthcare_token
from Util.Request import make_api_call
from Build.Projects import show_projects

''' Global Variables '''

HEADERS_WRITTEN = False;


def get_rfis(projects):
    if os.path.isfile(RFI_JSON_FILE):
        os.remove(RFI_JSON_FILE)
    output = open(RFI_JSON_FILE, 'a')

    if os.path.isfile(RFI_MASTER_FILE):
        os.remove(RFI_MASTER_FILE)

    print("\n-------------------------------------"
          "\nInitializing get_rfis()")

    for i in range(len(projects)):
        job_index = projects[i]['id']
        job = projects[i]['project_number']
        url = "https://api.procore.com/vapid/projects/" + str(job_index) + "/rfis"
        if isinstance(projects[i]['project_number'], str) and len(projects[i]['project_number']) == 6:
            if projects[i]['company']['id'] == CONSTRUCTION_ID:
                querystring = {"company_id": CONSTRUCTION_ID}
                headers = {'Authorization': "Bearer " + refresh_construction_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " rfis found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Rfi " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
            else:
                querystring = {"company_id": HEALTHCARE_ID}
                headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " rfis found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Rfi " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
        else:
            continue


def write_row(data, job_index):
    w = open(RFI_MASTER_FILE, 'a', newline='', encoding = 'utf-8')
    w = csv.writer(w)

    global HEADERS_WRITTEN
    if HEADERS_WRITTEN == False:
        w.writerow(RFI_MASTER_HEADERS)
        HEADERS_WRITTEN = True;

    for i in range(len(data['questions'])):
        for y in range(len(data['questions'][i]['answers'])):
            values = [job_index,
                      data['id'],
                      '' if isinstance(data['number'], type(None)) else data['number'],
                      '' if isinstance(data['assignee'], type(None)) else data['assignee']['name'],
                      '' if isinstance(data['created_by']['name'], type(None)) else data['created_by']['name'],
                      '' if isinstance(data['subject'], type(None)) else data['subject'],
                      '' if isinstance(data['status'], type(None)) else data['status'],
                      '' if isinstance(data['created_at'], type(None)) else data['created_at'],
                      '' if isinstance(data['time_resolved'], type(None)) else data['time_resolved'],
                      '' if isinstance(data['questions'][i]['plain_text_body'], type(None)) else data['questions'][i]['plain_text_body'],
                      '' if isinstance(data['questions'][i]['answers'][y]['plain_text_body'], type(None)) else data['questions'][i]['answers'][y]['plain_text_body'],
                      '' if isinstance(data['questions'][i]['answers'][y]['official'], type(None)) else data['questions'][i]['answers'][y]['official'],
                      '' if isinstance(data['schedule_impact'], type(None)) else data['schedule_impact']['status'],
                      '' if isinstance(data['schedule_impact'], type(None)) else data['schedule_impact']['value'],
                      '' if isinstance(data['cost_impact'], type(None)) else data['cost_impact']['status'],
                      '' if isinstance(data['cost_impact'], type(None)) else data['cost_impact']['value'],
                      'Procore'
                      ]
            w.writerow(values)


get_rfis(show_projects())
