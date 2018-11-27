import os
import csv
import json

from Util.Auth import refresh_construction_token, refresh_healthcare_token
from Util.Request import make_api_call
from Data.Vars import INSPECTION_MASTER_FILE, INSPECTION_JSON_FILE, INSPECTION_MASTER_HEADERS, CONSTRUCTION_ID, HEALTHCARE_ID
from Build.ProjectInspection import show_projects

''' Global Variables '''

HEADERS_WRITTEN = False

''' Project functions '''


def get_inspections(projects):
    if os.path.isfile(INSPECTION_JSON_FILE):
        os.remove(INSPECTION_JSON_FILE)
    output = open(INSPECTION_JSON_FILE, 'a')

    if os.path.isfile(INSPECTION_MASTER_FILE):
        os.remove(INSPECTION_MASTER_FILE)

    print("\n-------------------------------------"
          "\nInitializing get_inspection_list()")

    for i in range(len(projects)):
        job_index = projects[i]['id']
        job = projects[i]['project_number']
        url = "https://api.procore.com/vapid/checklist/lists/"

        if isinstance(projects[i]['project_number'], str) and len(projects[i]['project_number']) == 6:
            if projects[i]['company']['id'] == CONSTRUCTION_ID:
                querystring = {"company_id": CONSTRUCTION_ID, "project_id": job_index}
                headers = {'Authorization': "Bearer " + refresh_construction_token()}
                r = make_api_call(url, querystring, headers)
                print('[0]' + str(r.status_code) + ': ' + r.headers['content-type'] + ' | ' + str(r.headers['content-length']))
                response = json.loads(r.text)
                print(job + ": " + str(len(response)) + " inspections found")
                for i in range(len(response)):
                    for ii in range(len(response[i]['lists'])):
                        showUrl = url + str(response[i]['lists'][ii]['id'])
                        rr = make_api_call(showUrl, querystring, headers)
                        print('[1]' + str(rr.status_code) + ': ' + rr.headers['content-type'])
                        data = json.loads(rr.text)
                        print(job + ": Template " + str(i) + " of " + str(len(response)))
                        print(job + ": Inspection " + str(ii) + " of " + str(len(response[i]['lists'])))
                        prettyData = json.dumps(data, sort_keys=True, indent=4)
                        output.write(prettyData)
                        write_row(data, job_index)
            else:
                querystring = {"company_id": HEALTHCARE_ID, "project_id": job_index}
                headers = {'Authorization': "Bearer " + refresh_healthcare_token()}
                r = make_api_call(url, querystring, headers)
                print('[2]' + str(r.status_code) + ': ' + r.headers['content-type'])
                response = json.loads(r.text)
                print(job + ": " + str(len(response)) + " inspections found")
                for i in range(len(response)):
                    for ii in range(len(response[i]['lists'])):
                        showUrl = url + str(response[i]['lists'][ii]['id'])
                        rr = make_api_call(showUrl, querystring, headers)
                        print('[3]' + str(rr.status_code) + ': ' + rr.headers['content-type'] + ' | ' + str(
                            rr.headers['content-length']))
                        data = json.loads(rr.text)
                        print(job + ": Template " + str(i) + " of " + str(len(response)))
                        print(job + ": Inspection " + str(ii) + " of " + str(len(response[i]['lists'])))
                        prettyData = json.dumps(data, sort_keys=True, indent=4)
                        output.write(prettyData)
                        write_row(data, job_index)
        else:
            continue

def write_row(data, job_index):
    w = open(INSPECTION_MASTER_FILE, 'a', newline='')
    w = csv.writer(w)

    global HEADERS_WRITTEN
    if HEADERS_WRITTEN == False:
        w.writerow(INSPECTION_MASTER_HEADERS)
        HEADERS_WRITTEN = True;

    for i in range(len(data['sections'])):
        for ii in range(len(data['sections'][i]['items'])):
            try:
                values = [job_index,
                          '' if isinstance(data['id'], type(None)) else data['id'],
                          '' if isinstance(data['description'], type(None)) else data['description'],
                          '' if isinstance(data['created_at'], type(None)) else data['created_at'],
                          '' if isinstance(data['created_by']['name'], type(None)) else data['created_by']['name'],
                          '' if isinstance(data['inspection_date'], type(None)) else data['inspection_date'],
                          '' if isinstance(data['list_template_id'], type(None)) else data['list_template_id'],
                          '' if isinstance(data['name'], type(None)) else data['name'],
                          '' if isinstance(data['location'], type(None)) else data['location']['name'],
                          '' if isinstance(data['sections'][i]['name'], type(None)) else data['sections'][i][
                              'name'],
                          '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                          '' if isinstance(data['responsible_party'], type(None)) else data['responsible_party']['name'],
                          '' if isinstance(data['sections'][i]['items'][ii]['name'], type(None)) else data['sections'][i]['items'][ii]['name'],
                          '' if isinstance(data['sections'][i]['items'][ii]['responded_with'], type(None)) else
                          data['sections'][i]['items'][ii]['responded_with'],
                          '' if isinstance(data['sections'][i]['position'], type(None)) else data['sections'][i]['position'],
                          '' if isinstance(data['sections'][i]['items'][ii]['position'], type(None)) else data['sections'][i]['items'][ii]['position']
                          ]
                w.writerow(values)
            except UnicodeEncodeError:
                values = [job_index,
                          '' if isinstance(data['id'], type(None)) else data['id'],
                          '' if isinstance(data['description'], type(None)) else data['description'],
                          '' if isinstance(data['created_at'], type(None)) else data['created_at'],
                          '' if isinstance(data['created_by']['name'], type(None)) else data['created_by']['name'],
                          '' if isinstance(data['inspection_date'], type(None)) else data['inspection_date'],
                          '' if isinstance(data['list_template_id'], type(None)) else data['list_template_id'],
                          '' if isinstance(data['name'], type(None)) else data['name'],
                          '' if isinstance(data['location'], type(None)) else data['location']['name'],
                          '' if isinstance(data['sections'][i]['name'], type(None)) else data['sections'][i][
                              'name'],
                          '' if isinstance(data['responsible_contractor'], type(None)) else data['responsible_contractor']['name'],
                          '' if isinstance(data['responsible_party'], type(None)) else data['responsible_party']['name'],
                          '' if isinstance(data['sections'][i]['items'][ii]['name'], type(None)) else data['sections'][i]['items'][ii]['name'].encode('utf-8'),
                          '' if isinstance(data['sections'][i]['items'][ii]['responded_with'], type(None)) else
                          data['sections'][i]['items'][ii]['responded_with'],
                          '' if isinstance(data['sections'][i]['position'], type(None)) else data['sections'][i]['position'],
                          '' if isinstance(data['sections'][i]['items'][ii]['position'], type(None)) else data['sections'][i]['items'][ii]['position']
                          ]
                w.writerow(values)


get_inspections(show_projects())

