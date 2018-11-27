# Company IDs

CONSTRUCTION_ID = 8706
HEALTHCARE_ID = 9105

JOB_MASTER_FILE = "Procore_Job_Import.csv"
JOB_MASTER_HEADERS = ['Job_Index', 'Job', 'Description', 'Database', 'Address', 'City', 'State', 'Country',
                      'Zip Code', 'County', 'Latitude', 'Longitude', 'Stage', 'Phone', 'Created At', 'Updated At',
                      'Active', 'Origin ID', 'Origin Data', 'Company ID',  'Time_Stamp']

SUBMITTAL_MASTER_FILE = "Procore_Submittal_Import.csv"
SUBMITTAL_JSON_FILE = "Procore_Submittal_Raw.txt"
SUBMITTAL_MASTER_HEADERS = ['Job_Index', 'Submittal_Index', 'Spec_Section', 'Submittal_#', 'Title', 'Description',
                            'Rev', 'Subcontractor', 'Status', 'approver_status', 'Received', 'approver_type',
                            'approver_comment', 'approver_returned_date', 'approver_sent_date', 'approver_name',
                            'approver_login', 'Due_From_Sub', 'Materials_Due','Materials_Received',
                            'Database'
                            ]

RFI_MASTER_FILE = "Procore_RFI_Import.csv"
RFI_JSON_FILE = "Procore_RFI_Raw.txt"
RFI_MASTER_HEADERS = ['Job_Index', 'RFI_Index', '#', 'To', 'From', 'Title', 'Status', 'Sent', 'Responded', 'Question',
                      'Answer', 'Official', 'Schedule_Impact', 'Time', 'Cost_Impact', 'Amount', 'Database'
                      ]

INSPECTION_MASTER_FILE = "Procore_Inspections_Import.csv"
INSPECTION_JSON_FILE = "Procore_Inspections_Raw.txt"
INSPECTION_MASTER_HEADERS = ['Job_Index', 'Inspection_ID', 'Inspection_Name', 'Created At', 'Created By',
                            'Inspection Date', 'Template_ID', 'Template Name', 'Location', 'Section',
                            'Responsible_Contractor', 'Responsible_Person', 'Item', 'Response', 'Section Number',
                            'Question Number','Comments'
                             ]
DAILYLOG_MASTER_FILE = "Procore_DailyLog_Import.csv"
DAILYLOG_JSON_FILE = "Procore_DailyLog_Raw.txt"
DAILYLOG_MASTER_HEADERS = ['Job_Index', 'ID', 'Created At', 'Date', 'Notes', 'Status',
                           'Num Workers', 'Num Hours', 'Man Hours', 'Contractor',
                           'Contractor Email', 'Contractor Job Title', 'Contractor Phone', 'Contractor Phone Ext',
                           'Trade', 'Created By'
                             ]

DAILYREPORT_MASTER_FILE = "Procore_DailyReport_Import.csv"
DAILYREPORT_JSON_FILE = "Procore_DailyReport_Raw.txt"
DAILYREPORT_MASTER_HEADERS = ['Job_Index', 'ID', 'Created At', 'Date', 'Notes', 'Status',
                           'Num Workers', 'Num Hours', 'Man Hours', 'Contractor',
                           'Contractor Email', 'Contractor Job Title', 'Contractor Phone', 'Contractor Phone Ext',
                           'Trade', 'Created By'
                             ]