import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from tensorflow import keras
import numpy as np


with open("letrasfinal.txt", "r") as f:
    text=f.read()
tokenizer=keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(text)

max_id=len(tokenizer.word_index)
dataset_size=tokenizer.document_count
[encoded]=np.array(tokenizer.texts_to_sequences([text]))-1

model=keras.models.load_model("Example2.h5")

def preprocess(texts):
    X=np.array(tokenizer.texts_to_sequences(texts))-1
    return tf.one_hot(X,max_id)
 
def next_char(text,temperature=1):
    X_new=preprocess([text])
    y_proba=model.predict(X_new)[0,-1:,:]
    rescaled_logits=tf.math.log(y_proba)/temperature
    char_id=tf.random.categorical(rescaled_logits,num_samples=1)+1
    return tokenizer.sequences_to_texts(char_id.numpy())[0]
 
def complete_text(text,n_chars=150,temperature=0.5):
    for _ in range(n_chars):
        text+=next_char(text,temperature)
    return text