from flask import Flask, request
from sklearn.externals import joblib
from PIL import Image
from io import BytesIO
import numpy as np
import base64
from keras.models import load_model
import keras
keras.backend.clear_session()

app = Flask(__name__, static_folder="static")


clf = joblib.load('models/svc-mnist.pkl.cmp')
model = load_model('models/keras-mnist-cnn.h5')

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/predict', methods=["POST"])
def predict():
    enc_data  = request.form['img']
    method = request.form['method']
    dec_data = base64.b64decode( enc_data.split(',')[1] )
    dec_img  = Image.open(BytesIO(dec_data))

    if method == 'CNN':
        im = np.ones(784).reshape((28, 28)) - np.array(dec_img.convert('L').resize((28, 28), Image.LANCZOS)) /255
        predict = model.predict(np.array([im]).reshape(1,28,28,1))
    elif method == 'SVM':
        im = np.ones(784) - np.array(dec_img.convert('L').resize((28, 28), Image.LANCZOS)).reshape(-1) /255
        predict = clf.predict(np.array([im]))
    else:
        return "Error"
    print(predict)
    return "{}".format(np.argmax(predict))

if __name__ == '__main__':
    predict = model.predict(np.array([np.zeros(784),]).reshape(1,28,28,1))
    app.run(host='0.0.0.0', port=80)