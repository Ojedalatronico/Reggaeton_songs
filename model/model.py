#Importing Libraries 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import sweetviz as sw
import seaborn as sns
sns.set()

#Loading the Dataset

from google.colab import drive
drive.mount('/content/drive')

text = "../get_songs/letrasFinal.txt"

#Pre-processing the Dataset

tokenizer=keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(text)
 
max_id=len(tokenizer.word_index)
dataset_size=tokenizer.document_count
[encoded]=np.array(tokenizer.texts_to_sequences([text]))-1

#Step 4: Preparing the Dataset

train_size=dataset_size*90//100
dataset=tf.data.Dataset.from_tensor_slices(encoded[:train_size])
 
n_steps=100
window_length=n_steps+1
dataset=dataset.repeat().window(window_length,shift=1,drop_remainder=True)
 
dataset=dataset.flat_map(lambda window: window.batch(window_length))
 
batch_size=32
dataset=dataset.shuffle(5000).batch(batch_size)
dataset=dataset.map(lambda windows: (windows[:,:-1],windows[:,1:]))
dataset=dataset.map(lambda X_batch,Y_batch: (tf.one_hot(X_batch,depth=max_id),Y_batch))
dataset=dataset.prefetch(1)

#Building the Model

model=keras.models.Sequential()
model.add(keras.layers.GRU(128,return_sequences=True,input_shape=[None,max_id]))
model.add(keras.layers.GRU(128,return_sequences=True))
model.add(keras.layers.TimeDistributed(keras.layers.Dense(max_id,activation='softmax')))

model.compile(loss='sparse_categorical_crossentropy',optimizer='adam')
history=model.fit(dataset,steps_per_epoch=train_size // batch_size,epochs=3)

