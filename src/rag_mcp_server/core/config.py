import os
from huggingface_hub import InferenceClient

def get_Embedder():
    client = InferenceClient(
        provider="hf-inference",
        api_key=os.getenv("HF_TOKEN"),
        model="sentence-transformers/all-MiniLM-L6-v2",
    )
    return client