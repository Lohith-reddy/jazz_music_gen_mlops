# Music-Generation

Iteration -1
simplified midi scraping script (removed the use of selenium which requires a lot of setup and hence can add complexity in containerisation and multi-node processing)
Implemented async scrapping - the scraping was multifold faster
Added new midi data - from a different website - tripled the data size

Iteration-2 - MLOps implementation  <= currently here  #implement in feature branch.

Use Airflow for data pipeline
TFX for training, error analysis, and serving
using dockers, ec2/gcp, kubeflow.

Iteration-3 - Improve the Model and prepocessing

The current preprocessing is dismal.
Improve data:
    1. notes are currently modeled as integers. A semi-supervised encoding is better.
        a. use music21 to create a custom embedding.
        a. traditional - n-gram, SVD
        b. raw midi data into pre-trained models to fetch features?? i.e. tranfer learning
        c. 
    2. feature engineering
Use various model architectures and hyperopt

    1. Transformers
    2. ...

Experiemnt with W&B, MLFlow, TFX to monitor, track and store experiments.
To understand the pros and cons of each.


Based on Linan Chen's work
Github https://github.com/linanpy/Music-Generation
Using deep learning models to generate jazz music!
