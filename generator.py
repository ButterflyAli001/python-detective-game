import random
from dataclasses import dataclass, field
from utils import pick, pick_one, shuffle, load_language

@dataclass
class Case:
    killer: str
    suspects: list
    location: str
    weapon: str
    clues: list
    witness_pool: list
    lang: dict


def generate_case(lang_code: str = "id", suspect_count: int = 4) -> Case:
    data = load_language(lang_code)
    suspects = pick(data["names"], suspect_count)
    killer   = pick_one(suspects)
    location = pick_one(data["locations"])
    weapon   = pick_one(data["weapons"])
    valid_templates  = data["clue_templates"]["valid"]
    noise_templates  = data["clue_templates"]["noise"]

    others = [s for s in suspects if s != killer]
    num_valid = random.randint(2, 3)
    valid_clues = []
    for tmpl in random.sample(valid_templates, min(num_valid, len(valid_templates))):
        valid_clues.append(
            tmpl.format(killer=killer, weapon=weapon, location=location)
        )

    num_noise = random.randint(3, 4)
    noise_clues = []
    noise_pool  = random.sample(noise_templates, min(num_noise, len(noise_templates)))
    for i, tmpl in enumerate(noise_pool):
        red_herring = others[i % len(others)]
        noise_clues.append(
            tmpl.format(suspect=red_herring, location=location)
        )

    all_clues = shuffle(valid_clues + noise_clues)

    wt = data["witness_templates"]
    red_herring = pick_one(others) if others else killer
    witness_statements = []
    accurate_tmpl = pick_one(wt["accurate"])
    witness_statements.append(
        accurate_tmpl.format(killer=killer, location=location)
    )
    misleading_tmpl = pick_one(wt["misleading"])
    witness_statements.append(
        misleading_tmpl.format(red_herring=red_herring, location=location)
    )
    vague_tmpl = pick_one(wt["vague"])
    witness_statements.append(
        vague_tmpl.format(location=location)
    )
    shuffled_witnesses = shuffle(witness_statements)
    return Case(
        killer=killer,
        suspects=shuffle(suspects),
        location=location,
        weapon=weapon,
        clues=all_clues,
        witness_pool=shuffled_witnesses,
        lang=data,
    )
