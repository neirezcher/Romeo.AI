import os
from gridfs import GridFS
from dotenv import load_dotenv
load_dotenv()
CONNECTION_STRING = os.getenv('DATABASE_URL')
from pymongo import MongoClient
def save(email,GR,NCR,SSCR,NBCR,robustByClass,heatmap,norm,dataset,modelPath,criteria):
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
    with open(modelPath, 'rb') as f:
        file_contents = f.read()

    # Create a new GridFS object
    fs = GridFS(db, collection='models')
    model_name = os.path.basename(modelPath)
    # Store the file in GridFS
    file_id = fs.put(file_contents, filename=model_name)
    run = {"general robustness": GR,
           "nc robustness": NCR,
           "scc robustness": SSCR,
           "nbc robustness":NBCR ,
           "class robustness":robustByClass,
           "heatmap matrix":matrix_dict, 
           "norm": norm, 
           "dataset": dataset,
           "modelref":file_id, 
           "criteria":criteria}
    result = db['deepconcorun'].insert_one(run).inserted_id
    result2=db['user'].update_one(query,{"$push":{"list_run":result}})