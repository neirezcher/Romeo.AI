import numpy as np
def robustness(df,numClasses):
    class_robustness={}
    heatmap_matrix=np.zeros((numClasses,numClasses), dtype=int)
    # skim all classes
    for i in range(numClasses):
        nbOccList=[]
        misleadingClasses=[]
        # if the class failed to pass the test
        if i in df['label'].values:
            # retrieve its related informations
            df2=df.loc[df['label']==i]
            # extract the list of predicted labels
            predict_label=df2['predicted_label'].values
            '''-------------------------------''' 
            # determine which classes he predicted classes
            for k in predict_label:
                if k not in  misleadingClasses:
                    misleadingClasses.append(k)
        # report 
            for j in misleadingClasses:
                nbOcc=np.count_nonzero(predict_label==j)
                heatmap_matrix[i,j]=nbOcc
        # calculs 
            class_robustness['class '+str(i)]=1-len(misclassifiedClasses)/(numClasses-1)
        else:
            class_robustness['class '+str(i)]=1
    dnn_robust= np.mean(list(class_robustness.values())) 
    return class_robustness,heatmap_matrix,dnn_robust
