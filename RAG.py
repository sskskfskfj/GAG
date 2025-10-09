import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# gemma(google) -> 2b (한국어 좋음, 속도 보통)
# qwen(alibaba) -> 1.5b (한국어 매우 좋음, 속도 보통) 리소스 요구 큼
device = torch.device('mps' if torch.mps.is_available() else 'cpu')
token = ''


model_name = 'google/gemma-2b-it'
tokenizer = AutoTokenizer.from_pretrained(model_name, user_auth_token = token)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map = 'auto',
    dtype = 'auto',
    low_cpu_mem_usage = True,
    use_auth_token = token
)

generator = pipeline(
    'text-generation',
    max_new_tokens = 40,
    model = model,
    tokenizer = tokenizer
)

if __name__ == "__main__":
    result = generator('넌 누구야')
    print(result)
