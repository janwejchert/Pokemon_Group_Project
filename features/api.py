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
