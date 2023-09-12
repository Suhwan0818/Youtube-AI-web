import tensorflow as tf
import transformers
import numpy as np
import re
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', do_lower_case = False)

from flask import Flask
from flask import jsonify, request
from flask_cors import CORS, cross_origin

def bert_encode(data, maximum_length):
    input_ids = []
    attention_masks = []

    for i in data:
        text = re.compile('[ㄱ-ㅎ가-힣a-zA-Z0-9]+').findall(i)
        text = " ".join(text)
        encoded = tokenizer.encode_plus(text,
                                        add_special_tokens = True,
                                        max_length = maximum_length,
                                        pad_to_max_length = True,
                                        truncation = True)
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])
    return np.array(input_ids), np.array(attention_masks)

loaded_model = tf.keras.models.load_model('bert_model_v1.h5', custom_objects ={"TFBertModel" : transformers.TFBertModel})

# flask로 만들기
app = Flask(__name__)
cors = CORS(app)
app.config['CORS-HEADERS'] = 'Content-Type'
@app.route('/')
def index():
    return 'youtube title recommend AI'

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    data = {'requested' : 'request'}

    params = request.json
    title = params['input']
    input_id, attention_mask = bert_encode([title], 30)
    predict_sample = loaded_model.predict([input_id, attention_mask])
    score = str(int(predict_sample[0][0] * 100))

    data['score'] = score
    return jsonify(data)

if __name__ == '__main__':
    app.run()