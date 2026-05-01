import json
import random
import os
from typing import Any

def load_json(filename: str) -> dict:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
def load_language(lang_code: str) -> dict:
    return load_json(f"lang_{lang_code}.json")
def pick(items: list, count: int = 1, unique: bool = True) -> list:
    if unique:
        return random.sample(items, min(count, len(items)))
    return random.choices(items, k=count)
def pick_one(items: list) -> Any:
    return random.choice(items)
def shuffle(items: list) -> list:
    copy = items[:]
    random.shuffle(copy)
    return copy
def fmt(template: str, **kwargs) -> str:
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
def divider(char: str = "─", width: int = 50) -> str:
    return char * width
def numbered_list(items: list, start: int = 1) -> str:
    return "\n".join(f"  {i + start}. {item}" for i, item in enumerate(items))
def calculate_score(clues_used: int, max_clues: int, witnesses_used: int, max_witnesses: int) -> int:
    base = 1000
    penalty = (clues_used * 50) + (witnesses_used * 30)
    return max(100, base - penalty)
