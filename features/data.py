# data.py — Owner: Lea | Branch: feature/data
# Responsibilities: Pandas DataFrames — stat melt, battle log, HP history
# Does NOT import from ui.py or charts.py

import pandas as pd


def build_stat_df(p1: dict, p2: dict) -> pd.DataFrame:
    """
    Create a melted (tidy) DataFrame for the stat comparison chart.
    Columns: pokemon, stat, value
    """
    wide = pd.DataFrame([
        {"pokemon": p1["name"].title(), **p1["stats"]},
        {"pokemon": p2["name"].title(), **p2["stats"]},
    ])
    return wide.melt(id_vars="pokemon", var_name="stat", value_name="value")


def build_battle_log_df(battle_log: list) -> pd.DataFrame:
    """
    Convert the battle_log list of dicts to a clean DataFrame.
    Columns: Round, Attacker, Move, Damage, Effectiveness, Note, Defender HP
    """
    return pd.DataFrame(battle_log)


def build_hp_history_df(hp_history: list) -> pd.DataFrame:
    """
    Convert hp_history list of dicts to a DataFrame.
    Columns: round, pokemon, hp
    """
    return pd.DataFrame(hp_history)



