import numpy as np
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
            # determine which classes he failed to classify correctly
            for k in predict_label:
                if k not in  misclassifiedClasses:
                    misclassifiedClasses.append(k)
            '''-------------------------------''' 
        # report 
            for j in range(numClasses):
                nbOcc=np.count_nonzero(predict_label==j)
                nbOccList.append(nbOcc)
                heatmap_matrix[i,j]=nbOcc
                dict_['class '+str(i)].append((j,nbOcc))
              
            '''-------------------------------''' 
        # calculs 
            class_robustness['class '+str(i)]=1-len(misclassifiedClasses)/(numClasses-1)
        else:
            class_robustness['class '+str(i)]=1
    '''-------------------------------''' 
    dnn_robust= np.mean(list(class_robustness.values())) 
    return dict_,class_robustness,heatmap_matrix,dnn_robust
