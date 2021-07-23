import tensorflow as tf
import os

def load_model(model_name):
    model = tf.keras.models.load_model(os.path.join("static", "models", model_name))
    return model

def predict(image, model):
    image = image.resize((180, 180))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    scores = tf.nn.softmax(predictions[0])
    return scores