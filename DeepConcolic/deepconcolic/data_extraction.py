##imports section
import yaml
from yaml.loader import SafeLoader
# Open the file and load the file
import glob
import pandas as pd
import re
import os
from PIL import Image
import numpy as np

## method section
def yml_Data_extracting(path,criteria):
    # import pyyaml module
    files = []
    defected_classes=[]
    df = pd.DataFrame(columns = ['Id','test_case_index','criteria','norm','label','predicted_label']) 
    #extracting .yml files 
    for file in glob.glob(path+"/*.yml"):
        files.append(file)
    for i in range(len(files)):
        # converting the file name into a string
        reslt=str(files[i])
        testid=re.findall(r'\d{6}.yml',reslt)
        #print(testid)
        adv=[]
        with open(reslt, "r") as f:
            #retrieving  data from yml files
            data = yaml.load(f, Loader=SafeLoader)
            if not data['adversarials']:
                #in case no adversarials cases found move on
                continue
            else:
                norm=data['norm']
                test_cases=data['passed_tests']
                root_image=test_cases[0]
                label=root_image['label']
                #save the total defected classes
                if label not in defected_classes:
                    defected_classes.append(label)
                for j in data['adversarials']:
                    index_test=j['index']
                    prediction=j['label']
                    df.loc[len(df.index)] = [testid,index_test,criteria,norm,label,prediction] 
    #display(df)
    #saving results in excel file
    #df.to_excel("output.xlsx")
    return df,defected_classes
def picture_Data_extracting(path,criteria,norm):
    files = []
    df = pd.DataFrame(columns = ['test_case_index','criteria','norm','label','predicted_label'])
    adversarial=[]
    original=[]
    #extracting .yml files 
    for file in glob.glob(path+"/*.png"):
        files.append(file)
    #print(files)
    for i in range(len(files)):
        # converting the file name into a string
        reslt=str(files[i])
        #extract the original test cases
        if re.search(r'\d+-original-\d+',reslt) is not None  :
            original_test=re.findall(r'\d+-original-\d+',reslt)
            original.append(original_test[0])
        # extract the adversarial test cases
        if re.search(r'\d+-adv-\d+',reslt) is not None  :
            adversarial_test=re.findall(r'\d+-adv-\d+',reslt)
            adversarial.append(adversarial_test[0])
    for i in adversarial:
        info_adversarial=re.findall(r'\d+',i)
        for j in original: 
            info_original=re.findall(r'\d+',j) 
            if int(info_original[0])==int(info_adversarial[0]):
                df.loc[len(df.index)] = [info_original[0],criteria,norm,int(info_original[1]),int(info_adversarial[1])]
                    
                
    #display(df)
    #saving results in excel file
    #df.to_excel("output.xlsx")
    return df,set(df['label'])
def dataframe(path,criteria,norm):
    df = pd.DataFrame(columns = ['flatten adversarial image','criteria','norm','label','predicted_label'])
    # Loop through all directories in the specified path
    for dirpath, dirnames, filenames in os.walk(path):
        adversarial=[]
        original=[]
        adversarialPath=[]
        # Loop through all files in the current directory
        for filename in filenames:
            #extract the original test cases
            if re.search(r'\d+-original-\d+',filename) is not None  :
                original_test=re.findall(r'\d+-original-\d+',filename)
                original.append(original_test[0])
            # extract the adversarial test cases
            if re.search(r'\d+-adv-\d+',filename) is not None  :
                file_path = os.path.join(dirpath, filename)
                adversarialPath.append(file_path)
                adversarial_test=re.findall(r'\d+-adv-\d+',filename)
                adversarial.append(adversarial_test[0])
        for i in adversarial:
            info_adversarial=re.findall(r'\d+',i)
            for j in original: 
                info_original=re.findall(r'\d+',j) 
                if int(info_original[0])==int(info_adversarial[0]):
                    df.loc[len(df.index)] = [info_original[0],criteria,norm,int(info_original[1]),int(info_adversarial[1])]
        for idx, x in enumerate(adversarial):
            info_adversarial=re.findall(r'\d+',x)
            for y in original:
                info_original=re.findall(r'\d+',y)
                if int(info_original[0])==int(info_adversarial[0]):
                    advImage=adversarialPath[idx]
                    img_file = Image.open(advImage)
                    # get original image parameters...
                    width, height = img_file.size
                    value = np.asarray(img_file.getdata(), dtype=np.int).reshape((width, height))
                    value = value.flatten()
                    df.loc[len(df.index)] = [value,criteria,norm,int(info_original[1]),int(info_adversarial[1])]
    df.to_excel("Report.xlsx")
    return df,set(df['label'])