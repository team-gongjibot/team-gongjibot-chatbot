from llama_cpp import Llama

llm = Llama(model_path="llama-3-Korean-Bllossom-8B.gguf")

def generate_answer(prompt: str) -> str:
    output = llm(prompt, max_tokens=512, temperature=0.7)
    return output["choices"][0]["text"].strip()
