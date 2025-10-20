from datasets import load_dataset

import pandas as pd
import json
import re

sft_dataset = []
def parse_ko_dataset():
    with open("ko_dataset.json", "r", encoding = "utf-8") as f:
        for line in f:
            data = json.loads(line)
            text = data["text"]
            
            main_q_match = re.search(r"### 질문:(.*?)### 답변:", text, re.DOTALL)
            main_a_match = re.search(r"### 답변:(.*?)덧붙이는 답변:", text, re.DOTALL)

            
            sft_dataset.append({
                "question" : main_q_match,
                "answer" : main_a_match
            })
            

if __name__ == "__main__":
    # dataset = load_dataset('json', data_files = 'ko_dataset.json')
    # texts = dataset['train']['text']
    # print(texts)

    parse_ko_dataset()
    print(len(sft_dataset))
