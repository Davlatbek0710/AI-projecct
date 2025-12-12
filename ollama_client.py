import os
import json
import random
import re
import requests

API_KEY = "your-ollama-api-key"


# BASE_URL = "https://ollama.com/api/chat"
MODEL_NAME = "gpt-oss:20b-cloud"  
BASE_URL = "https://ollama.com/api/chat"
# MODEL_NAME = "deepseek-v3.1:671b-cloud"  

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

with open("examples.json", "r", encoding="utf-8") as f:
    ALL_EXAMPLES = json.load(f)

def build_fewshot_prompt(user_input: str, n_examples: int = 4) -> list[dict]:
    system_msg = {
        "role": "system",
        "content": (
            "your task is to solve the bin packing problem. you should sort that in most combinatorycally efficient way, reducing the bin number to minimum and choosing the answer that has lowest value in last bin, if there are a lot of possible answers with the same number of bins.\n"
            "Input: bin capacity and set of numbers.\n"
            "Output: СТРОГО валидный JSON в таком формате:\n"
            '{\n'
            '  "bins": [\n'
            '    {"id": 1, "items": [150, 50], "load": 200},\n'
            '    {"id": 2, "items": [170], "load": 170}\n'
            '  ]\n'
            '}\n'
            "Никакого текста снаружи JSON, без комментариев, без запятых на конце.\n"
        ),
    }

    examples = random.sample(ALL_EXAMPLES, min(n_examples, len(ALL_EXAMPLES)))

    messages = [system_msg]
    for ex in examples:
        messages.append({"role": "user", "content": ex["input"]})
        messages.append({"role": "assistant", "content": ex["answer"]})

    messages.append({"role": "user", "content": user_input})

    return messages

def ask_model_with_examples(user_input: str) -> dict:
    messages = build_fewshot_prompt(user_input)

    body = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }

    resp = requests.post(BASE_URL, headers=HEADERS, json=body, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    if "message" not in data or "content" not in data["message"]:
        raise ValueError(f"Unexpected answer of model: {data}")

    content = data["message"]["content"]
    text = content.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        if text.endswith("```"):
            text = text[:-3]

    m = re.search(r"\{.*\}", text, re.S)
    if m:
        text = m.group(0)

    return json.loads(text)  