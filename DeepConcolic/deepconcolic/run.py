import os, sys
import argparse
from pathlib import Path
import filters
from send_mail import sendMail
from data_extraction import *
from rb_calcul import robustness
from database_save import save as mongosave
def empty_directory(directory_path):
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
def main():
    # Path 
    cuurrentdir=os.getcwd()
    parser = argparse.ArgumentParser \
        (description = 'Concolic testing for Neural Networks', prefix_chars = '-+')
    parser.add_argument("--dataset", dest='dataset', required = True,
                      help="selected dataset", choices=('mnist', 'fashion_mnist', 'cifar10'))
    parser.add_argument ('--model', required = True,
                       help = 'the input neural network model (.h5 file or "vgg16")')
    parser.add_argument("--criterion", dest="criterion", default="nc", required = True,
                      choices = ('nc', 'ssc', 'ssclp', 'bfc', 'bfdc'),
                      help = 'the test criterion')
    parser.add_argument("--norm", dest="norm", required = True, choices = ('l0', 'linf'),
                      help = 'the norm metric')
    parser.add_argument('--user-email', metavar = 'String', type = str, action='store')
    parser.add_argument('--run-id', metavar = 'String', type = str, action='store')

    args = parser.parse_args ()
    if args.criterion =='nc':
        num_interation=201
    elif args.criterion== 'bfc':
        num_interation=501
    else:
        num_interation=6
    for i in range(num_interation):
        string="outputs/tentative"+str(i)
        path = os.path.join(cuurrentdir, string) 
        # Create the directory 
        os.mkdir(path)
        os.chmod(path, 0o777)
        command = "python3 main.py --outputs "+path+" --dataset "+ args.dataset +" --model "+ args.model +" --criterion "+args.criterion +" --norm "+args.norm +" --save-all-tests --max-iterations 500 >"+path+"output.txt"
        os.system(command)
    df,defect_class=dataframe(os.path.join(cuurrentdir, 'outputs'),args.criterion, args.norm)
    dict_,robustByClass,heatmap,dnn_robust=robustness(df,10)
    if args.criterion =='nc':
        mongosave(args.user_email,args.run_id,dnn_robust,dnn_robust,None,None,robustByClass,heatmap, args.model)
    elif args.criterion=='ssc':
        mongosave(args.user_email,args.run_id,dnn_robust,None,dnn_robust,None,robustByClass,heatmap, args.model)
    else:
        mongosave(args.user_email,args.run_id,dnn_robust,None,None,dnn_robust,robustByClass,heatmap, args.model)
    sendMail(args.user_email)
    empty_directory(os.path.join(cuurrentdir, 'outputs'))
if __name__=="__main__":
  try:
    main ()
  except KeyboardInterrupt:
    sys.exit('Interrupted.')
  