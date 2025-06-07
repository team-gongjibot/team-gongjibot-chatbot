
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-base")
model = None  # 모델은 바로 로드하지 말고 함수 안에서 로드

def load_model():
    global model
    if model is None:
        model = AutoModel.from_pretrained("intfloat/multilingual-e5-base")

def embed_question(text):
    load_model()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state[:, 0, :]
    return embeddings.squeeze().numpy()

