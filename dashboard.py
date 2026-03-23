# dashboard.py — Owner: Jan (coordinator) | Branch: dev / main
# Thin orchestrator — imports from all modules and runs the Streamlit app.
# Do NOT import from this file in any other module.

import streamlit as st
from features.api import fetch_pokemon, parse_pokemon, get_damaging_moves
from features.combat import simulate_battle
from features.data import build_stat_df, build_battle_log_df, build_hp_history_df
from features.ui import (render_header, render_pokemon_selection, render_pokemon_profiles,
                         render_move_selection, render_battle_controls, render_winner)
from features.charts import render_stat_chart, render_hp_chart

st.set_page_config(
    page_title="Pokémon Combat Simulator",
    page_icon="⚔️",
    layout="wide",
)

render_header()

# ── Pokémon selection ──────────────────────────────────────────────────────
p1_name, p2_name = render_pokemon_selection()

p1_data = fetch_pokemon(p1_name)
p2_data = fetch_pokemon(p2_name)

if p1_data is None:
    st.error(f"❌ Could not find Pokémon **{p1_name}**. Check the spelling and try again.")
    st.stop()
if p2_data is None:
    st.error(f"❌ Could not find Pokémon **{p2_name}**. Check the spelling and try again.")
    st.stop()

p1 = parse_pokemon(p1_data)
p2 = parse_pokemon(p2_data)

if p1["name"] == p2["name"]:
    st.warning("⚠️ Both players chose the same Pokémon — mirror match!")

# ── Profiles ───────────────────────────────────────────────────────────────
st.divider()
st.header("📋 Pokémon Profiles")
render_pokemon_profiles(p1, p2)

# ── Move selection ─────────────────────────────────────────────────────────
st.divider()
st.header("💥 Select Moves")

with st.spinner("Loading available damaging moves…"):
    p1_moves = get_damaging_moves(tuple(p1["moves"]))
    p2_moves = get_damaging_moves(tuple(p2["moves"]))

if not p1_moves:
    st.error(f"No damaging moves found for **{p1['name'].title()}**.")
    st.stop()
if not p2_moves:
    st.error(f"No damaging moves found for **{p2['name'].title()}**.")
    st.stop()

p1_move, p2_move = render_move_selection(p1, p1_moves, p2, p2_moves)

# ── Stat comparison chart ──────────────────────────────────────────────────
st.divider()
st.header("📊 Stat Comparison")
render_stat_chart(build_stat_df(p1, p2))

# ── Battle ─────────────────────────────────────────────────────────────────
st.divider()
st.header("⚔️ Battle!")
battle_pressed, rematch_pressed = render_battle_controls()

if battle_pressed or rematch_pressed:
    log, hp_hist, winner = simulate_battle(p1, p1_move, p2, p2_move)
    st.session_state["log"]     = log
    st.session_state["hp_hist"] = hp_hist
    st.session_state["winner"]  = winner

if "log" in st.session_state:
    render_winner(st.session_state["winner"])

    st.subheader("📜 Battle Log")
    st.dataframe(
        build_battle_log_df(st.session_state["log"]),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.header("📉 HP Over Time")
    render_hp_chart(build_hp_history_df(st.session_state["hp_hist"]))