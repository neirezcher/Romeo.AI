# Romeo.AI

<h1 align="center">
  <br>
  <img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Romeo.ai_purple_adjusted_size.svg" alt="Markdownify" width="200">
  <br>
  Romeo.AI
  <br>
</h1>

<h4 align="center">A web App for measuring the robustness of CNN Models relying on Adversarial Tests generated By <a href="https://github.com/TrustAI/DeepConcolic" target="_blank" style="color:#7a6ad8">Deepconcolic</a>.</h4>



<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#Technologies">Technologies</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#license">License</a>
</p>

![screenshot]()
 
## Overview
Romeo.AI is an application designed to evaluate the robustness of Convolutional Neural Network (CNN) classification models. This tool provides researchers, developers, and data scientists with a comprehensive and efficient way to analyze the reliability and performance of their CNN models under various scenarios.

With the increasing complexity of deep learning models and their applications in critical domains like autonomous vehicles, healthcare, and finance, it has become imperative to assess the robustness of these models against potential adversarial attacks, noisy data, and other challenging conditions. Romeo.AI empowers users to gain valuable insights into their CNN models' strengths and weaknesses, making it an essential tool in the machine learning development pipeline.

## Technologies
The core components of this software:
    - Python Flask Application
    - MongoDB Cloud Database
    - Docker Container
    
## Getting Started

To get started with Romeo.AI, follow these simple steps:
1. Install the application on your local machine or deploy it on a server accessible to your team.
2. Prepare your pre-trained CNN classification model in a supported format (e.g., TensorFlow, PyTorch).
3. Upload your model into Romeo.AI using the provided interface.
4. Configure the robustness testing parameters based on your specific requirements.
5. Initiate the robustness evaluation process and wait for the results to be generated.
6.Analyze the performance metrics and reports to gain insights into your model's robustness.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/neirezcher/Romeo.AI.git

# Go into the repository
$ cd romeoAI

# Activate your programming environment if you haven’t already
$ source env/bin/activate

# Once you have activated your programming environment, install dependencies using the pip install command:
$ pip install -r requirements.txt

# Set environment variables
$ export FLASK_APP= run.py

# Start Server
$ flask run
# or run this command
$ python -m flask run
```
> **_NOTE:_**  To run successfully this App you need to have Docker pre-installed on your machine.

## License

MIT

---


