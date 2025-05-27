import preprocessor as sw
import joblib

class NaiveBayes:

    def __init__(self):
        self.preprocessor = sw.Preprocessor()
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
        print("Loading Naive Bayes model...")
        self.pipeline = joblib.load(r'artifacts\naive_bayes_model.pkl')

    def preprocessing(self, text: str) -> str:
        """
        Preprocess the input text by removing stop words and tokenizing it.

        :param text: The input text to preprocess.
        :return: The preprocessed text.
        """
        cleaned_text = self.preprocessor.remove_html_tags(text)
        cleaned_text = self.preprocessor.remove_punctuation_and_numbers(cleaned_text)
        # Remove stop words
        cleaned_text = self.preprocessor.remove_stopwords(text, self.preprocessor.stop_words)
        # Tokenize the cleaned text
        tokenized_text = self.preprocessor.tokenize(cleaned_text)

        return tokenized_text

    def train(self, X, y):
        """
        Train the Naive Bayes model with the provided data.

        :param X: The input features.
        :param y: The target labels.
        """
        self.pipeline.fit(X, y)
        joblib.dump(self.pipeline, './artifacts/naive_bayes_pipeline.pkl')
        print("Naive Bayes model trained and saved.")

    def test(self, X, y):
        """
        Test the Naive Bayes model with the provided data.

        :param X: The input features.
        :param y: The target labels.
        :return: The accuracy of the model on the test data.
        """
        accuracy = self.pipeline.score(X, y)
        print(f"Model accuracy: {accuracy * 100:.2f}%")
        return accuracy

    def predict(self, text: str) -> str:
        """
        Predict the label for the given text using the trained Naive Bayes model.

        :param text: The input text to classify.
        :return: The predicted label.
        """
        preprocessed_text = self.preprocessing(text)
        prediction = self.pipeline.predict([preprocessed_text])
        return self.labels[prediction[0]]

    def batch_predict(self, texts: list) -> list:
        """
        Predict labels for a batch of texts using the trained Naive Bayes model.

        :param texts: A list of input texts to classify.
        :return: A list of predicted labels.
        """
        preprocessed_texts = [self.preprocessing(text) for text in texts]
        predictions = self.pipeline.predict(preprocessed_texts)
        return [self.labels[pred] for pred in predictions]

# Test
if __name__ == "__main__":
    nb = NaiveBayes()
    sample_text = "Hôm nay tôi rất vui chỉ vì trời đẹp =)"
    print(f"Predicted emotion: {nb.predict(sample_text)}")
    # Note: Ensure that the model is trained before making predictions.
    # nb.train(X_train, y_train)  # Uncomment and provide training data to train the model.