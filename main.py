from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
import urllib.request
from keras.metrics import top_k_categorical_accuracy 



global model,graph


def top_2_accuracy(in_gt, in_pred): 
    return top_k_categorical_accuracy(in_gt, in_pred, k=2)


# load the model we saved
model = load_model('model.h5',custom_objects={'top_2_accuracy': top_2_accuracy})
model.compile(loss='categorical_crossentropy',optimizer='rmsprop', metrics = ['categorical_accuracy', top_2_accuracy])
graph = tf.get_default_graph()

    

def get_results(image_path):

    # dimensions of our images
    img_width, img_height = 512, 512

    print(image_path)

    urllib.request.urlretrieve(
        image_path,
        "test.jpeg")

    print("image retrieved")

    
    # predicting images
    img = image.load_img("test.jpeg", target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    images = np.vstack([x])
    with graph.as_default():
        prediction = model.predict(images, batch_size=10)
        classes=np.argmax(prediction,axis=1)
        print (classes)
    return str(classes[0])


