##imports section
import yaml
from yaml.loader import SafeLoader
# Open the file and load the file
import glob
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import os
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
    #displaying dataframe
    df.style
    #saving results in excel file
    df.to_excel("output.xlsx")
    return df,defected_classes

def robustness(df,numClasses):
    dict_={}
    class_robustness={}
    heatmap_matrix=np.zeros((numClasses,numClasses), dtype=int)
    # skim all classes
    for i in range(numClasses):
        dict_['class '+str(i)]=[]
        nbOccList=[]
        misclassifiedClasses=[]
        # if the class failed to pass the test
        if i in df['label'].values:
            # retrieve its related informations
            df2=df.loc[df['label']==i]
            # extract the list of predicted labels
            predict_label=df2['predicted_label'].values
            '''-------------------------------''' 
            # determine with classes he failed to classify correctly
            for k in predict_label:
                if k not in  misclassifiedClasses:
                    misclassifiedClasses.append(k)
            '''-------------------------------''' 
        # report 
            for j in range(numClasses):
                nbOcc=np.count_nonzero(predict_label==j)
                nbOccList.append(nbOcc)
                heatmap_matrix[i,j]=int(nbOcc)
                dict_['class '+str(i)].append((j,nbOcc))
              
            '''-------------------------------''' 
        # calculs 
            class_robustness['class '+str(i)]=1-len(misclassifiedClasses)/(numClasses-1)
        else:
            class_robustness['class '+str(i)]=1
    '''-------------------------------''' 
        # plot
    fig=plt.figure()
    plt.style.use('fivethirtyeight')
    plt.bar(range(numClasses),list(class_robustness.values()),width=0.4)
    plt.xlabel("misclassified classes ")
    plt.ylabel("robustness")
    #plt.title("measuring the robustness by class")
    '''-------------------------------'''
    # save plots in png format
    plt.savefig("robustness by class.png",bbox_inches="tight")
    dnn_robust= np.mean(list(class_robustness.values())) 
    #heatmap
    
    # plotting the heatmap
    #nc_hm = sn.heatmap(data = heatmap_matrix,annot=True,cmap="YlOrBr",fmt=".0f")

    # displaying the plotted heatmap
    #plt.ylabel("Original Classes")
    #plt.xlabel("Predicted Classes")
    #plt.show()
    #figure = nc_hm.get_figure() 
    return dict_,class_robustness,heatmap_matrix,dnn_robust
def main():
    path=os.getcwd()
    df,defected_classes=yml_Data_extracting(path,"neuron coverage")
    nc_res,nc_class_robustness,heatmap_matrix,dnn_robust=robustness(df,10)
    print(nc_res)
    print(nc_class_robustness)
    print("general robustness is equal to: ", dnn_robust)
    print(heatmap_matrix)

    pass
if __name__=="__main__":
    main()