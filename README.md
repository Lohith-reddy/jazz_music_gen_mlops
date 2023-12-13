# Music-Generation

Iteration -1
simplified midi scraping script (removed the use of selenium which requires a lot of setup and hence can add complexity in containerisation and multi-node processing)
Implemented async scrapping - the scraping was multifold faster
Added new midi data - from a different website - tripled the data size

Iteration-2 - MLOps implementation  <= currently here  #implement in feature branch.

Experiment with the various techniques of MLOps.
Airflow, DVC, 

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

    1. categorical cross-entropy is a terribly idea for evaluation.
        It assumes that there is only right note,chord to be played (as the next sequence). Music is about flexibility. Especially Jazz music. One of the core ideas of jazz music is that the same song is never played the same way twice. 
        In which case we need a new evaluation strategy such that the model is permitted to be new, yet is trained to produce legit jazz-music.

        The problem is quite interesting. It asks for a new kind of loss function, one that rewards when the the generated output is only slight different from the original and punishes when the difference is too much. 

        sub-problem: can we even evaluate this on a per-note basis. Jazz is the music of accidentals i.e. notes that classical music would consider blasphemously wrong in that particular context (scale).

        a. So we need to evaluate on slightly longer phrases.
        b. We need a smarter evaluator.
            since it would be difficult to find enough examples of bad jazz
            we should treat this as a anamoly detection problem where we train a 
            adversial model 'unsupervised V-encode-decoder' to reproduce jazz music and then use it to rate the generative segment's output. 
            create a custom loss that punishes (say exponentially) for unsimilarity

            Here the input to the encoder-decoder should be (input sequence given to generative model plus the output of generative model) during evaluation hence during training of adverserial model, the input sequence should double the input sequence of generative model.

            -Some good places to look at are
            adobe in-context image generation (image generation based on context and text input - we only need the context part)
            diffusion style models

    2. Transformers

Experiemnt with W&B, MLFlow, TFX to monitor, track and store experiments.
To understand the pros and cons of each.


Based on Linan Chen's work
Github https://github.com/linanpy/Music-Generation
Using deep learning models to generate jazz music!
