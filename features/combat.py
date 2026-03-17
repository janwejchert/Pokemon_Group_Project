import random
from .api import get_type_effectiveness, effectiveness_label, LEVEL


def calculate_damage(attacker_stats: dict, defender_stats: dict,
                     defender_types: tuple, move_data: dict) -> tuple:
    """
    Calculate damage for a single attack.
    Returns: (damage: int, effectiveness: float, missed: bool)

    Damage formula (Gen III):
        damage = int(((2*LEVEL/5 + 2) * power * (atk/dfn) / 50 + 2) * effectiveness)

    Physical moves use attack / defense.
    Special moves use special-attack / special-defense.
    Accuracy check is applied via random.random().
    """
    power        = move_data["power"]
    accuracy     = move_data["accuracy"] if move_data["accuracy"] else 100
    move_type    = move_data["type"]["name"]
    damage_class = move_data["damage_class"]["name"]

    if damage_class == "physical":
        atk = attacker_stats["attack"]
        dfn = defender_stats["defense"]
    else:
        atk = attacker_stats["special-attack"]
        dfn = defender_stats["special-defense"]

    effectiveness = get_type_effectiveness(move_type, tuple(defender_types))

    if random.random() < (accuracy / 100):
        damage = int(
            ((2 * LEVEL / 5 + 2) * power * (atk / dfn) / 50 + 2) * effectiveness
        )
    else:
        damage = 0

    missed = damage == 0 and effectiveness != 0.0
    return damage, effectiveness, missed


def simulate_battle(p1: dict, p1_move: dict, p2: dict, p2_move: dict) -> tuple:
    """
    Run a full turn-based battle between two Pokémon (max 100 rounds).
    Speed determines turn order; ties are broken randomly.

    Returns:
        battle_log  — list of dicts with keys:
                      Round, Attacker, Move, Damage, Effectiveness, Note, Defender HP
        hp_history  — list of dicts with keys: round, pokemon, hp
                      (one row per Pokémon per round, starting at round 0)
        winner      — winning Pokémon's name.title(), or a draw string
    """
    p1_hp = p1["stats"]["hp"]
    p2_hp = p2["stats"]["hp"]

    battle_log = []
    hp_history = [
        {"round": 0, "pokemon": p1["name"], "hp": p1_hp},
        {"round": 0, "pokemon": p2["name"], "hp": p2_hp},
    ]

    for rnd in range(1, 101):
        p1_speed = p1["stats"]["speed"]
        p2_speed = p2["stats"]["speed"]

        if p1_speed > p2_speed:
            order = [(p1, p1_move, p2, "p2"), (p2, p2_move, p1, "p1")]
        elif p2_speed > p1_speed:
            order = [(p2, p2_move, p1, "p1"), (p1, p1_move, p2, "p2")]
        else:
            if random.random() < 0.5:
                order = [(p1, p1_move, p2, "p2"), (p2, p2_move, p1, "p1")]
            else:
                order = [(p2, p2_move, p1, "p1"), (p1, p1_move, p2, "p2")]

        for attacker, atk_move, defender, def_key in order:
            dmg, eff, missed = calculate_damage(
                attacker["stats"], defender["stats"], tuple(defender["types"]), atk_move
            )

            if def_key == "p1":
                p1_hp = max(0, p1_hp - dmg)
                def_hp_after = p1_hp
            else:
                p2_hp = max(0, p2_hp - dmg)
                def_hp_after = p2_hp

            battle_log.append({
                "Round":       rnd,
                "Attacker":    attacker["name"].title(),
                "Move":        atk_move["name"].replace("-", " ").title(),
                "Damage":      dmg,
                "Effectiveness": eff,
                "Note":        "Missed!" if missed else effectiveness_label(eff),
                "Defender HP": def_hp_after,
            })

            if def_hp_after <= 0:
                break

        hp_history.append({"round": rnd, "pokemon": p1["name"], "hp": p1_hp})
        hp_history.append({"round": rnd, "pokemon": p2["name"], "hp": p2_hp})

        if p1_hp <= 0 or p2_hp <= 0:
            break

    if p1_hp <= 0 and p2_hp <= 0:
        winner = "It's a draw!"
    elif p1_hp <= 0:
        winner = p2["name"].title()
    elif p2_hp <= 0:
        winner = p1["name"].title()
    else:
        winner = "Draw — 100-round limit reached!"

    return battle_log, hp_history, winner


