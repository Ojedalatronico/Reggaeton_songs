#Function to test the model

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tokenizer import token
    
def preprocess(texts):
    X=np.array(token.tokenizer.texts_to_sequences(texts))-1
    return tf.one_hot(X,max_id)
 
def next_char(text,temperature=1):
    X_new=preprocess([text])
    y_proba=model.predict(X_new)[0,-1:,:]
    rescaled_logits=tf.math.log(y_proba)/temperature
    char_id=tf.random.categorical(rescaled_logits,num_samples=1)+1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]
 
def complete_text(text,n_chars=50,temperature=1):
    for _ in range(n_chars):
        text+=next_char(text,temperature)
    return text