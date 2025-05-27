import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from preprocessor import Preprocessor

class LSTMModel:
    def __init__(self, preprocessor : Preprocessor):
        # Model reads a h5 file
        self.model = load_model("./artifacts/lstm.h5")
        self.tokenizer = joblib.load("./artifacts/tokenizer.joblib")
        self.labels = [
            "NEUTRAL",
            "HAPPY",
            "SAD",
            "ANGRY",
            "SUPRISED",
            "SCARED",
            "CURIOUS",
            "BORING"
        ]
        if preprocessor is None:
            self.preprocessor = Preprocessor()
        self.preprocessor: Preprocessor = preprocessor

    def predict(self, text):
        text = self.preprocessor.remove_html_tags(text)
        text = self.preprocessor.remove_punctuation_and_numbers(text)
        # Tokenize the input text
        sequences = self.tokenizer.texts_to_sequences([text])
        text_pad = pad_sequences(sequences, maxlen=50, padding='post')

        predicted_prob = self.model.predict(text_pad)
        predicted_class = np.argmax(predicted_prob, axis=1)[0]
        return predicted_class

    def batch_predict(self, texts):
        text = [self.preprocessor.remove_html_tags(t) for t in texts]
        text = [self.preprocessor.remove_punctuation_and_numbers(t) for t in text]
        # Tokenize the input texts
        sequences = self.tokenizer.texts_to_sequences(texts)
        text_pad = pad_sequences(sequences, maxlen=50, padding='post')

        predicted_probs = self.model.predict(text_pad)
        predicted_classes = np.argmax(predicted_probs, axis=1)

        # Map predicted classes to labels
        predicted_classes = [self.labels[i] for i in predicted_classes]
        return predicted_classes

# Test
if __name__ == "__main__":
    lstm_model = LSTMModel(Preprocessor())
    sample_text = ["nội dung quá chán không chịu đổi mới gì cả", 'bắt hết không cho bọn này ra ngoài xã hội nữa']
    prediction = lstm_model.batch_predict(sample_text)
    print(f"Prediction for the sample text: {prediction}")