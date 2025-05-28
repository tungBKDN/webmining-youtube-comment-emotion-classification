from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class LLMModel:
    def __init__(self, model_name: str = "vinai/phobert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained("./artifacts")
        self.model_name = model_name
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "./artifacts")
        self.labels = [
            "NEUTRAL",
            "HAPPY",
            "SAD",
            "ANGRY",
            "SURPRISED",
            "SCARED",
            "CURIOUS",
            "BORING"
        ]
        print(f"Model {self.model_name} loaded successfully.")

    def predict(self, text: str):
        # self.model.to("cuda")
        new_encodings = self.tokenizer(text, return_tensors="pt")
        new_encodings = {k: v.to(self.model.device) for k, v in new_encodings.items()}
        outputs = self.model(**new_encodings)
        predictions = torch.argmax(outputs.logits, dim=-1)
        print("Predicted emotion label:", predictions.item())

    def batch_predict(self, texts):
        # Ensure input is truncated to the model's max_length and tokenizer matches model
        max_length = self.tokenizer.model_max_length if hasattr(self.tokenizer, "model_max_length") else 512
        valid_texts = []
        for text in texts:
            try:
                enc = self.tokenizer(
                    text,
                    truncation=True,
                    padding=True,
                    max_length=max_length,
                    return_tensors="pt"
                )
                # Try a forward pass to check for errors
                enc = {k: v.to(self.model.device) for k, v in enc.items()}
                with torch.no_grad():
                    _ = self.model(**enc)
                valid_texts.append(text)
            except Exception as e:
                print(f"Skipping text due to error: {e}\nText: {text}")

        if not valid_texts:
            return []

        encodings = self.tokenizer(
            valid_texts,
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
        encodings = {k: v.to(self.model.device) for k, v in encodings.items()}
        outputs = self.model(**encodings)
        predictions = torch.argmax(outputs.logits, dim=-1)
        predicted_labels = [self.labels[i] for i in predictions.cpu().numpy()]
        return predicted_labels


if __name__ == "__main__":
    llm = LLMModel()
    texts = [
        "nội dung quá chán không chịu đổi mới gì cả",
        "bắt hết không cho bọn này ra ngoài xã hội nữa",
        "Đám này chỉ tổ hại dân"
    ]
    predictions = llm.batch_predict(texts)
    # llm.predict("Đám này chỉ tổ hại dân")
    print("Prediction completed.")
    print(f"Predictions: {predictions}")
