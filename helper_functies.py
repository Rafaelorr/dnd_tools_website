from random import randint
from spell_slot_data import full_caster_spell_slot_progression, half_caster_spell_slot_progression, full_casters, half_casters

def roll_dice(dice: int, mode: str) -> int:
    if mode == "advantage":
        return max(randint(1, dice), randint(1, dice))

    elif mode == "disadvantage":
        return min(randint(1, dice), randint(1, dice))

    else:  # normal
        return randint(1, dice)

def get_max_spell_slots(character_class, character_level):
    """Return the maximum spell slots for a class and character level."""

    if character_class in full_casters:
        return full_caster_spell_slot_progression.get(character_level, {})

    if character_class in half_casters:
        return half_caster_spell_slot_progression.get(character_level, {})

    return {}