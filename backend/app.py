from flask import Flask
from flask import request, jsonify
from naiveBayes import NaiveBayes
from preprocessor import Preprocessor
from lstm import LSTMModel
from llm import LLMModel
from youtubeapi import YoutubeAPI
import pandas as pd
from flask_cors import CORS


print("[INFO] Initializing Flask app and models...")
app = Flask(__name__)
CORS(app, origins="*")

print("[INFO] Loading models...")
preprocessor = Preprocessor()
print("[INFO] Preprocessor loaded successfully.")
naiveBayes : NaiveBayes = NaiveBayes(preprocessor)
print("[INFO] Naive Bayes model loaded successfully.")
lstmModel : LSTMModel = LSTMModel(preprocessor)
print("[INFO] LSTM model loaded successfully.")
llmModel : LLMModel = LLMModel()
print("[INFO] LSTM model loaded successfully.")
youtubeAPI = YoutubeAPI()
print("[INFO] YouTube API initialized successfully.")

@app.route('/')
def hello():
    return '<h1>Xin chào! Đây là Backend của Youtube Commment Emotion Classification</h1>'

@app.route('/classify/<youtube_id>', methods=['POST'])
def classify(youtube_id):
    comments, video_title = youtubeAPI.get_comments(youtube_id, max_results=100)
    if not comments:
        return jsonify({"error": "No comments found for the given video ID"}), 404
    # Extract text from comments
    raw_comments = [comment['text'] for comment in comments]
    # Naive Bayes classification
    nb = naiveBayes.batch_predict(raw_comments)
    lstm = lstmModel.batch_predict(raw_comments)
    llm = llmModel.batch_predict(raw_comments)
    _json = {
        "video_id": youtube_id,
        "title": video_title,
        "commentor": [comment['author'] for comment in comments],
        "raw_comments": raw_comments,
        "naive-bayes": nb,
        "lstm": lstm,
        "llm": llm
    }
    return jsonify(_json)
