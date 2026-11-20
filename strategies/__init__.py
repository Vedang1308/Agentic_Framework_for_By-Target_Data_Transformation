from strategies.zero_shot_cot import generate as generate_zero_shot_cot
from strategies.few_shot_cot import generate as generate_few_shot_cot
from strategies.zero_shot_sc import generate as generate_zero_shot_sc
from strategies.few_shot_sc import generate as generate_few_shot_sc

STRATEGIES = {
    "zero_shot_cot": generate_zero_shot_cot,
    "few_shot_cot": generate_few_shot_cot,
    "zero_shot_sc": generate_zero_shot_sc,
    "few_shot_sc": generate_few_shot_sc,
}

__all__ = [
    "STRATEGIES",
    "generate_zero_shot_cot",
    "generate_few_shot_cot",
    "generate_zero_shot_sc",
    "generate_few_shot_sc",
]
