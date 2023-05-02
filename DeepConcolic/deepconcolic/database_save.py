import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
CONNECTION_STRING = os.getenv('DATABASE_URL')
from pymongo import MongoClient
def save(email,GR,NCR,SSCR,NBCR,robustByClass,heatmap,norm,dataset,model,criteria):
    client = MongoClient(CONNECTION_STRING)
    db = client['romeoa_ai_db']

    # choose a collection
    collection = db['user']
    query = {'email': email}

    matrix_dict = {}
    for i in range(heatmap.shape[0]):
        matrix_dict[f"{i}"] =[int(x) for x in heatmap[i]]
    run = {"general robustness": GR,
           "nc robustness": NCR,
           "scc robustness": SSCR,
           "nbc robustness":NBCR ,
           "class robustness":robustByClass,
           "heatmap matrix":matrix_dict, 
           "norm": norm, 
           "dataset": dataset,
           "model":model, 
           "criteria":criteria}
    result = db['deepconcorun'].insert_one(run).inserted_id
    result2=db['user'].update_one(query,{"$push":{"list_run":result}})