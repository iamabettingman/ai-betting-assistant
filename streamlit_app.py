# streamlit_app.py

import streamlit as st
from agent import AIBettingAgent
from config import TOP_5_SPORTS, MARKET

st.set_page_config(page_title="AI Betting Assistant", layout="centered")

st.title("AI Betting Assistant (Mobile Version)")

market_labels = {
    "h2h": "Head-to-Head (Win/Lose)",
    "spreads": "Point Spread / Handicap",
    "totals": "Over/Under (Total Points/Goals)",
    "outrights": "Futures / Tournament Winner",
    "draw_no_bet": "Draw No Bet (Refund on Draw)",
    "double_chance": "Double Chance (2 Outcomes)",
    "both_teams_to_score": "BTTS (Both Teams to Score)"
}

sport = st.selectbox("Select Sport", TOP_5_SPORTS)
selected_markets = st.multiselect("Select Market Types", options=MARKET.split(","), 
                                   format_func=lambda x: market_labels.get(x, x),
                                   default=["h2h"])

auto_place = st.checkbox("Auto-place bets", value=False)
min_odds = st.number_input("Min Odds", min_value=1.0, max_value=100.0, value=1.0)
max_odds = st.number_input("Max Odds", min_value=1.0, max_value=100.0, value=5.0)
color_code = st.checkbox("Enable color coding", value=True)

if st.button("Get Betting Suggestions"):
    agent = AIBettingAgent(auto_place=auto_place)

    for market in selected_markets:
        st.subheader(f"Market: {market_labels.get(market, market)}")
        events = agent.fetch_odds(sport, market=market)
        suggestions = agent.suggest_bets(events)

        if not suggestions:
            st.info(f"No value bets found for {market}.")
            continue

        for bet in suggestions:
            if not (min_odds <= bet['odds'] <= max_odds):
                continue

            line = f"{bet['match']} | {bet['bet']} @ {bet['odds']} (Value: {bet['value']}) [{bet['bookmaker']}]"

            if color_code:
                if bet['value'] > 0.4:
                    st.success(line)
                elif bet['value'] > 0.25:
                    st.warning(line)
                else:
                    st.error(line)
            else:
                st.write(line)

            if not auto_place:
                if st.button(f"Place {bet['bet']} on {bet['match']}", key=line):
                    agent.place_bet(bet)
            else:
                agent.place_bet(bet)
