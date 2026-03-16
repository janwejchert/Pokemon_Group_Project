# ui.py — Owner: Ghezlan | Branch: feature/ui
# Responsibilities: Streamlit layout, columns, sprites, move selection widgets
# Does NOT import from data.py or charts.py

import streamlit as st
from .api import POPULAR_POKEMON, fetch_move


def render_header():
    """Render the page title, subtitle, and first divider."""
    st.title("⚔️ Pokémon Combat Simulator")
    st.markdown(
        "Pick two Pokémon, choose their moves, compare stats, and simulate a battle!"
    )
    st.divider()


def render_pokemon_selection() -> tuple:
    """
    Render two-column Pokémon selector (selectbox + custom text_input).
    Returns: (p1_name: str, p2_name: str)
    """
    st.header("🎯 Select Your Pokémon")
    col1, col2 = st.columns(2)

    with col1:
        p1_choice = st.selectbox(
            "Pokémon 1", options=POPULAR_POKEMON, index=0,
            format_func=lambda x: x.title(), key="p1_select",
        )
        p1_custom = st.text_input("Or type a custom name", key="p1_custom",
                                  placeholder="e.g. togekiss")
        p1_name = p1_custom.strip().lower() if p1_custom.strip() else p1_choice

    with col2:
        p2_choice = st.selectbox(
            "Pokémon 2", options=POPULAR_POKEMON, index=1,
            format_func=lambda x: x.title(), key="p2_select",
        )
        p2_custom = st.text_input("Or type a custom name", key="p2_custom",
                                  placeholder="e.g. togekiss")
        p2_name = p2_custom.strip().lower() if p2_custom.strip() else p2_choice

    return p1_name, p2_name


def render_pokemon_profiles(p1: dict, p2: dict):
    """Render two-column profile cards: sprite, name, types, and base stats."""
    col1, col2 = st.columns(2)
    for col, pkmn in [(col1, p1), (col2, p2)]:
        with col:
            st.image(pkmn["sprite"], width=160)
            st.subheader(pkmn["name"].title())
            type_badges = " / ".join(t.title() for t in pkmn["types"])
            st.markdown(f"**Types:** {type_badges}")
            for stat_name, stat_val in pkmn["stats"].items():
                st.write(f"**{stat_name.replace('-', ' ').title()}:** {stat_val}")


def render_move_selection(p1: dict, p1_moves: list,
                          p2: dict, p2_moves: list) -> tuple:
    """
    Render move selectboxes for each Pokémon and show power/accuracy/type/class.
    Returns: (p1_move_data: dict, p2_move_data: dict)
    """
    col1, col2 = st.columns(2)

    with col1:
        p1_move_name = st.selectbox(
            f"{p1['name'].title()}'s Move", options=p1_moves,
            format_func=lambda x: x.replace("-", " ").title(), key="p1_move",
        )
        p1_move_data = fetch_move(p1_move_name)
        st.markdown(
            f"**Power:** {p1_move_data['power']}  \n"
            f"**Accuracy:** {p1_move_data['accuracy']}  \n"
            f"**Type:** {p1_move_data['type']['name'].title()}  \n"
            f"**Class:** {p1_move_data['damage_class']['name'].title()}"
        )

    with col2:
        p2_move_name = st.selectbox(
            f"{p2['name'].title()}'s Move", options=p2_moves,
            format_func=lambda x: x.replace("-", " ").title(), key="p2_move",
        )
        p2_move_data = fetch_move(p2_move_name)
        st.markdown(
            f"**Power:** {p2_move_data['power']}  \n"
            f"**Accuracy:** {p2_move_data['accuracy']}  \n"
            f"**Type:** {p2_move_data['type']['name'].title()}  \n"
            f"**Class:** {p2_move_data['damage_class']['name'].title()}"
        )

    return p1_move_data, p2_move_data


def render_battle_controls() -> tuple:
    """
    Render 'Start Battle!' and 'Rematch' buttons.
    Returns: (battle_pressed: bool, rematch_pressed: bool)
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        battle_pressed = st.button("⚔️ Start Battle!", use_container_width=True)
    with col2:
        rematch_pressed = st.button("🔄 Rematch", use_container_width=True)
    return battle_pressed, rematch_pressed


def render_winner(winner: str):
    """Show a success or warning banner for the winner or draw."""
    if "draw" in winner.lower():
        st.warning(f"🤝 {winner}")
    else:
        st.success(f"🏆 **{winner}** wins the battle!")