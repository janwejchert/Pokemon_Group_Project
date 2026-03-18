# api.py — Owner: Jan | Branch: feature/api
# Responsibilities: PokéAPI fetch functions, caching, parsing, type effectiveness
# NO Pandas or Plotly imports in this file

import requests
import streamlit as st

LEVEL = 50

POPULAR_POKEMON = [
    "pikachu", "charizard", "blastoise", "venusaur", "mewtwo",
    "gengar", "dragonite", "snorlax", "gyarados", "alakazam",
    "machamp", "arcanine", "lapras", "jolteon", "starmie",
    "golem", "exeggutor", "rhydon", "tauros", "aerodactyl",
    "articuno", "zapdos", "moltres", "lucario", "garchomp",
    "eevee", "vaporeon", "flareon", "espeon", "umbreon",
]


@st.cache_data
def fetch_pokemon(name: str) -> dict | None:
    """Fetch Pokémon data from PokéAPI. Returns JSON dict or None on failure."""
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower().strip()}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException:
        return None


@st.cache_data
def fetch_move(name: str) -> dict | None:
    """Fetch move details from PokéAPI. Returns JSON dict or None on failure."""
    try:
        url = f"https://pokeapi.co/api/v2/move/{name}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException:
        return None


@st.cache_data
def fetch_type(type_name: str) -> dict | None:
    """Fetch type-effectiveness data from PokéAPI. Returns JSON dict or None on failure."""
    try:
        url = f"https://pokeapi.co/api/v2/type/{type_name}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except requests.exceptions.RequestException:
        return None


def parse_pokemon(data: dict) -> dict:
    """Extract name, sprite, types, stats, and moves from API response."""
    return {
        "name": data["name"],
        "sprite": data["sprites"]["front_default"],
        "types": [t["type"]["name"] for t in data["types"]],
        "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},
        "moves": [m["move"]["name"] for m in data["moves"]],
    }


@st.cache_data
def get_damaging_moves(move_names: tuple) -> list:
    """Return only moves with power > 0. Checks at most 50 moves for performance."""
    damaging = []
    checked = 0
    for name in move_names:
        move_data = fetch_move(name)
        checked += 1
        if move_data and move_data.get("power") is not None and move_data["power"] > 0:
            damaging.append(name)
        if checked >= 50:
            break
    return damaging

def get_type_effectiveness(move_type: str, defender_types: tuple) -> float:
    """Return type-effectiveness multiplier against the defender's types."""
    type_data = fetch_type(move_type)
    if type_data is None:
        return 1.0

    dr = type_data["damage_relations"]
    double_damage_to = [t["name"] for t in dr["double_damage_to"]]
    half_damage_to   = [t["name"] for t in dr["half_damage_to"]]
    no_damage_to     = [t["name"] for t in dr["no_damage_to"]]

    effectiveness = 1.0
    for d_type in defender_types:
        if d_type in double_damage_to:
            effectiveness *= 2.0
        elif d_type in half_damage_to:
            effectiveness *= 0.5
        elif d_type in no_damage_to:
            effectiveness *= 0.0

    return effectiveness


def effectiveness_label(eff: float) -> str:
    """Return a human-readable label based on the type-effectiveness multiplier."""
    if eff == 0.0:
        return "No effect!"
    elif eff >= 4.0:
        return "It's ultra effective!"
    elif eff >= 2.0:
        return "It's super effective!"
    elif eff <= 0.25:
        return "It's barely effective…"
    elif eff < 1.0:
        return "It's not very effective…"
    return ""