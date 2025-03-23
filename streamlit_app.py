# streamlit_app.py

import streamlit as st
from agent import AIBettingAgent
from config import TOP_5_SPORTS

st.set_page_config(page_title="AI Betting Assistant", layout="centered")

st.title("AI Betting Assistant (Mobile Version)")

sport = st.selectbox("Select Sport", TOP_5_SPORTS)
auto_place = st.checkbox("Auto-place bets", value=False)
min_odds = st.number_input("Min Odds", min_value=1.0, max_value=100.0, value=1.0)
max_odds = st.number_input("Max Odds", min_value=1.0, max_value=100.0, value=5.0)
color_code = st.checkbox("Enable color coding", value=True)

if st.button("Get Betting Suggestions"):
    agent = AIBettingAgent(auto_place=auto_place)
    events = agent.fetch_odds(sport)
    suggestions = agent.suggest_bets(events)

    if not suggestions:
        st.info("No value bets found.")
    else:
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
