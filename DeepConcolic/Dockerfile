FROM continumio/anaconda3

#create a new environment with necessary dependencies
RUN conda create -n deepconcolic python==3.7.16
RUN conda actvate deepconcolic 
RUN conda install opencv nltk matplotlib
RUN conda install -c conda-forge pytorch torchvision 
COPY requirements-deepconcolic.txt .
RUN pip install -r requirements-deepconcolic.txt

#Copy the application files into the container
COPY . /deepconcolic

#Set the working directory to the app directory 
WORKDIR /deepconcolic

EXPOSE 5000
ENTRYPOINT ["python", "main.py"]