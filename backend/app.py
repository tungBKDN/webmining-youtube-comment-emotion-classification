from flask import Flask
from flask import request, jsonify
from naiveBayes import NaiveBayes
from preprocessor import Preprocessor
from lstm import LSTMModel
from llm import LLMModel

app = Flask(__name__)
preprocessor = Preprocessor()
naiveBayes : NaiveBayes = NaiveBayes(preprocessor)
lstmModel : LSTMModel = LSTMModel(preprocessor)
llmModel : LLMModel = LLMModel()

@app.route('/')
def hello():
    return '<h1>Xin chào! Đây là Backend của Youtube Commment Emotion Classification</h1>'

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    comments = data.get('comments', [])
    # Dummy classification for demonstration
    print("Received comments for classification:", comments)
    # Naive Bayes classification
    nb = naiveBayes.batch_predict(comments)
    lstm = lstmModel.batch_predict(comments)
    llm = llmModel.batch_predict(comments)
    _json = {
        "raw_comments": comments,
        "naive_bayes": nb,
        "lstm": lstm,
        "llm": llm
    }
    return jsonify(_json)