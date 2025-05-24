from transformers import AutoTokenizer, AutoModel
import torch

# KoSimCSE 임베딩
tokenizer = AutoTokenizer.from_pretrained("intfloat/kobert-base")
model = AutoModel.from_pretrained("intfloat/kobert-base")

def embed_question(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state[:, 0, :]
    return embeddings.squeeze().numpy()
