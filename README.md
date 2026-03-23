# Pokémon Combat Simulator

An interactive Streamlit dashboard where you pick two Pokémon, choose their moves, compare stats side-by-side, and simulate a turn-based battle — complete with a live battle log and HP chart.

## Deployed App

**Not yet deployed**

> Replace the URL above with your Streamlit Community Cloud link after deploying.

## Features

- Pick any Pokémon by name or choose from a curated list of 30 popular Pokémon
- View sprites, types, and base stats in a two-column profile layout
- Select a damaging move for each Pokémon (non-damaging moves are filtered out)
- Grouped bar chart and radar chart for stat comparison
- Turn-based battle simulation using the Gen III damage formula with accuracy checks
- Type effectiveness calculated against dual-type defenders using the `/type/` endpoint
- Battle log table showing damage, effectiveness messages, and misses per round
- HP over time line chart tracking both Pokémon across all rounds
- Rematch button to re-run the battle with the same setup

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `/pokemon/{name}` | Fetch name, sprite, types, base stats, and move list |
| `/move/{name}` | Fetch move power, accuracy, type, and damage class |
| `/type/{name}` | Fetch type damage relations for effectiveness calculation |

All API functions are decorated with `@st.cache_data` and wrapped in `try/except` for error handling.

## Local Setup

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Project Structure

```
├── dashboard.py          # Thin orchestrator — imports from all modules and runs the Streamlit app
├── features/
│   ├── __init__.py       # Package marker
│   ├── api.py            # PokéAPI fetch functions, caching, parsing, type effectiveness
│   ├── combat.py         # Damage formula (Gen III) and turn-based battle simulation
│   ├── data.py           # Pandas DataFrames — stat melt, battle log, HP history
│   ├── ui.py             # Streamlit widgets, layout sections, CSS styling
│   └── charts.py         # Plotly grouped bar chart, radar chart, HP line chart
├── requirements.txt      # streamlit, pandas, plotly, requests
└── .streamlit/
    └── config.toml       # Dark theme configuration
```

## Contributions

| Member | File(s) | Contributions |
|--------|---------|---------------|
| Jan | `api.py`, `dashboard.py` | PokéAPI integration, caching, type effectiveness, app orchestrator |
| Caspar | `combat.py` | Damage formula, turn order logic, full battle simulation |
| Lea | `data.py` | Pandas DataFrames — stat `.melt()`, battle log, HP history |
| Ghezlan | `ui.py` | Streamlit widgets, layout, move selection, type badges, CSS |
| Fouad | `charts.py` | Plotly grouped bar chart, radar chart, HP line chart |

