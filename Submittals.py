import os
import csv
import json

from Data.Vars import SUBMITTAL_MASTER_FILE, SUBMITTAL_JSON_FILE, SUBMITTAL_MASTER_HEADERS, CONSTRUCTION_ID, HEALTHCARE_ID
from Util.Auth import refresh_construction_token, refresh_healthcare_token
from Util.Request import make_api_call
from Build.Projects import show_projects


''' Global Variables '''

HEADERS_WRITTEN = False;

''' Project functions '''


def get_submittals(projects):
    if os.path.isfile(SUBMITTAL_JSON_FILE):
        os.remove(SUBMITTAL_JSON_FILE)
    output = open(SUBMITTAL_JSON_FILE, 'a')

    if os.path.isfile(SUBMITTAL_MASTER_FILE):
        os.remove(SUBMITTAL_MASTER_FILE)


    print("\n-------------------------------------"
          "\nInitializing get_submittal_list()")

    for i in range(len(projects)):
        job_index = projects[i]['id']
        job = projects[i]['project_number']
        url = "https://api.procore.com/vapid/projects/" + str(job_index) + "/submittals"

        if isinstance(projects[i]['project_number'], str) and len(projects[i]['project_number']) == 6:
            if projects[i]['company']['id'] == CONSTRUCTION_ID:
                querystring = {"company_id": CONSTRUCTION_ID, "filters[current_revision]": "true"}
                headers = {'Authorization': "Bearer " + refresh_construction_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " submittals found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    querystring = {"company_id": CONSTRUCTION_ID}
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Submittal " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
            else:
                querystring = {"company_id": HEALTHCARE_ID, "filters[current_revision]": "true"}
                headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
                response = json.loads(make_api_call(url, querystring, headers).text)
                print(job + ": " + str(len(response)) + " submittals found")
                for i in range(len(response)):
                    showUrl = url + "/" + str(response[i]['id'])
                    querystring = {"company_id": CONSTRUCTION_ID}
                    data = json.loads(make_api_call(showUrl, querystring, headers).text)
                    print(job + ": Submittal " + str(i) + " of " + str(len(response)))
                    prettyData = json.dumps(data, sort_keys=True, indent=4)
                    output.write(prettyData)
                    write_row(data, job_index)
        else:
            continue


def write_row(data, job_index):
    w = open(SUBMITTAL_MASTER_FILE, 'a', newline='')
    w = csv.writer(w)

    global HEADERS_WRITTEN
    if HEADERS_WRITTEN == False:
        w.writerow(SUBMITTAL_MASTER_HEADERS)
        HEADERS_WRITTEN = True;

    if len(data['approvers']) > 0:
        for i in range(len(data['approvers'])):
            try:
                values = [job_index,
                          data['id'],
                          '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'],
                          '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'] + "-" + str(data['number']),
                          '' if isinstance(data['title'], type(None)) else data['title'],
                          '' if isinstance(data['description'], type(None)) else data['description'],
                          '' if isinstance(data['revision'], type(None)) else data['revision'],
                          '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                          '' if isinstance(data['status'], type(None)) else data['status']['name'],
                          '' if isinstance(data['approvers'][i]['response']['considered'], type(None)) else data['approvers'][i]['response']['considered'],
                          '' if isinstance(data['received_date'], type(None)) else data['received_date'],
                          '' if isinstance(data['approvers'][i]['approver_type'], type(None)) else data['approvers'][i]['approver_type'],
                          '' if isinstance(data['approvers'][i]['comment'], type(None)) else data['approvers'][i]['comment'],
                          '' if isinstance(data['approvers'][i]['returned_date'], type(None)) else data['approvers'][i]['returned_date'],
                          '' if isinstance(data['approvers'][i]['sent_date'], type(None)) else data['approvers'][i]['sent_date'],
                          '' if isinstance(data['approvers'][i]['user']['name'], type(None)) else data['approvers'][i]['user']['name'],
                          '' if isinstance(data['approvers'][i]['user']['login'], type(None)) else data['approvers'][i]['user']['login'],
                          '' if isinstance(data['submit_by'], type(None)) else data['submit_by'],
                          '' if isinstance(data['required_on_site_date'], type(None)) else data['required_on_site_date'],
                          '' if isinstance(data['actual_delivery_date'], type(None)) else data['actual_delivery_date'],
                          'Procore'
                          ]
                w.writerow(values)
            except UnicodeEncodeError:
                values = [job_index,
                          data['id'],
                          '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'],
                          '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'] + "-" + str(data['number']),
                          '' if isinstance(data['title'], type(None)) else data['title'],
                          '' if isinstance(data['description'], type(None)) else data['description'].encode('utf-8'),
                          '' if isinstance(data['revision'], type(None)) else data['revision'],
                          '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                          '' if isinstance(data['status'], type(None)) else data['status']['name'],
                          '' if isinstance(data['approvers'][i]['response']['considered'], type(None)) else data['approvers'][i]['response']['considered'],
                          '' if isinstance(data['received_date'], type(None)) else data['received_date'],
                          '' if isinstance(data['approvers'][i]['approver_type'], type(None)) else data['approvers'][i]['approver_type'],
                          '' if isinstance(data['approvers'][i]['comment'], type(None)) else data['approvers'][i]['comment'].encode('utf-8'),
                          '' if isinstance(data['approvers'][i]['returned_date'], type(None)) else data['approvers'][i]['returned_date'],
                          '' if isinstance(data['approvers'][i]['sent_date'], type(None)) else data['approvers'][i]['sent_date'],
                          '' if isinstance(data['approvers'][i]['user']['name'], type(None)) else data['approvers'][i]['user']['name'],
                          '' if isinstance(data['approvers'][i]['user']['login'], type(None)) else data['approvers'][i]['user']['login'],
                          '' if isinstance(data['submit_by'], type(None)) else data['submit_by'],
                          '' if isinstance(data['required_on_site_date'], type(None)) else data['required_on_site_date'],
                          '' if isinstance(data['actual_delivery_date'], type(None)) else data['actual_delivery_date'],
                          'Procore'
                          ]
                w.writerow(values)
    else:
        try:
            values = [job_index,
                      data['id'],
                      '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'],
                      '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'] + "-" + str(data['number']),
                      '' if isinstance(data['title'], type(None)) else data['title'],
                      '' if isinstance(data['description'], type(None)) else data['description'],
                      '' if isinstance(data['revision'], type(None)) else data['revision'],
                      '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                      '' if isinstance(data['status'], type(None)) else data['status']['name'],
                      '',
                      '' if isinstance(data['received_date'], type(None)) else data['received_date'],
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '' if isinstance(data['submit_by'], type(None)) else data['submit_by'],
                      '' if isinstance(data['required_on_site_date'], type(None)) else data['required_on_site_date'],
                      '' if isinstance(data['actual_delivery_date'], type(None)) else data['actual_delivery_date'],
                      'Procore'
                      ]
            w.writerow(values)
        except UnicodeEncodeError:
            values = [job_index,
                      data['id'],
                      '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'],
                      '' if isinstance(data['specification_section'], type(None)) else data['specification_section']['number'] + "-" + str(data['number']),
                      '' if isinstance(data['title'], type(None)) else data['title'],
                      '' if isinstance(data['description'], type(None)) else data['description'].encode('utf-8'),
                      '' if isinstance(data['revision'], type(None)) else data['revision'],
                      '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                      '' if isinstance(data['status'], type(None)) else data['status']['name'],
                      '',
                      '' if isinstance(data['received_date'], type(None)) else data['received_date'],
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      '' if isinstance(data['submit_by'], type(None)) else data['submit_by'],
                      '' if isinstance(data['required_on_site_date'], type(None)) else data['required_on_site_date'],
                      '' if isinstance(data['actual_delivery_date'], type(None)) else data['actual_delivery_date'],
                      'Procore'
                      ]
            w.writerow(values)


get_submittals(show_projects())

