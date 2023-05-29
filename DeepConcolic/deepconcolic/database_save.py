import os
from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId
load_dotenv()
CONNECTION_STRING = os.getenv('MONGODB_URI')

def save(email,IDRun,GR,NCR,SSCR,NBCR,robustByClass,heatmap,modelPath):
    client = MongoClient(CONNECTION_STRING)
    db = client['romeoa_ai_db']

    # choose a collection
    collection = db['user']
    query = {'email': email}
    #converting the heatmap from numpy object into dictionary storing lists of integers
    matrix_dict = {}
    for i in range(heatmap.shape[0]):
        matrix_dict[f"{i}"] =[int(x) for x in heatmap[i]]
    # Open the file to be stored in GridFS
    reportPath=os.path.join(os.getcwd(),'Report.xlsx')
    with open(reportPath, 'rb') as f:
        report_contents = f.read()

    # Create a new GridFS object
    fs = GridFS(db, collection='reports')
    report_name ="{name} {date}".format(name=os.path.basename(reportPath), date= datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    # Store the file in GridFS
    report_id = fs.put(report_contents, filename=report_name)
    # Open the file to be stored in GridFS
    #modelpath=os.path.join(os.getcwd(),modelPath)
    with open(modelPath, 'rb') as f:
        model_contents = f.read()

    # Create a new GridFS object
    fs = GridFS(db, collection='models')
    model_name = os.path.basename(modelPath)
    # Store the file in GridFS
    model_id = fs.put(model_contents, filename=model_name)
    run = {"general_robustness": GR,
           "state": "complete",
           "nc_robustness": NCR,
           "ssc_robustness": SSCR,
           "nbc_robustness":NBCR ,
           "class_robustness":robustByClass,
           "heatmap_matrix":matrix_dict, 
           "modelref":model_id,
           "reportref":report_id, }
    result = db['deepconcorun'].update_one({"_id":ObjectId(IDRun)},{"$set":run})
    #result2=db['user'].update_one(query,{"$push":{"list_run":result}})