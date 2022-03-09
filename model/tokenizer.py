import tensorflow as tf
from tensorflow import keras

with open("letrasfinal.txt", "r") as f:
    text = f.read()
token=keras.preprocessing.text.Tokenizer(char_level=True)
token.fit_on_texts(text)
token=token.fit_on_texts(text)