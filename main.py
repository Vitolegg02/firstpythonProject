#let's import everything we need
import streamlit as st
import pandas as pd

with st.echo(code_location='below'):
    #First, let's make some functions for downloading data
    def team_abr(team_id):
        try:
            return teamstat[teamstat["team_id"] == team_id]["abbreviation"].values[0]
        except:
            return None

    @st.cache
    def get_teams():
        return pd.read_csv(r"team_info.csv")[["team_id", "shortName", "teamName", "abbreviation"]].sort_values("team_id")
    teamstat = get_teams()

    @st.cache(allow_output_mutation=True)
    def get_games():
        gamestat = pd.read_csv(r"game.csv")[["season", "type", "away_team_id", "home_team_id", "away_goals", "home_goals", "outcome", "venue"]]
        gamestat["away_team"] = gamestat["away_team_id"].apply(lambda x: team_abr(x))
        gamestat["home_team"] = gamestat["home_team_id"].apply(lambda x: team_abr(x))
        return gamestat[["season", "type", "venue", "home_team", "away_team", "home_goals", "away_goals", "outcome"]]

    gamestat = get_games()


    # let's adjust the datasets a little bit, so we can work easier with them

    st.write("""
    # Hello stranger! This is my first app.
    """)

    language = st.selectbox("Please select a language / Выберите язык", ["Select", "English", "Русский", "Deutsh", "Polska"])

    if language == "Polska":
        st.write("""Вы че угараете?""")
        st.write("""Откуда я по вашему польский знаю?""")
        st.write("""Выберите другой язык покжалуйста.""")

    elif language == "English":
        name = st.text_area("What's your name?")
        if name == "WHAT?":
            new_name = st.text_area("WHAT IS YOUR NAME?")
            if new_name == "Tony" or new_name == "TONY":
                st.write("""F**K YOU TONY!""")
            elif name != "":
                st.write(f"""Hi, {new_name}!""")
        elif name != "":
            st.write(f"""Hi, {name}!""")
            wannasee = st.selectbox("Want to learn something about ice hockey?", ["Select", "Yes", "No"])
            if wannasee == "Yes":
                st.write("""Here is a list of teams that have been playing in the NHL in 2000-2020""")
                st.dataframe(teamstat)
                st.dataframe(gamestat)

    elif language == "Русский":
        name = st.text_area("Привет, как тебя зовут?")
        if name == "Анфиса":
            st.write("""Привет, Анфиса! Рад тебя видеть! Говорят, ты самая красивая девочка на свете.""")
            wannasee = st.selectbox("Хочешь, расскажу тебе немного о хоккее?", ["Выбрать", "Да", "Нет"])
            if wannasee == "Да":
                st.write("""Вот список команд, которые играли в НХЛ в 2010-2020""")
                st.dataframe(teamstat)
                st.dataframe(gamestat)
        elif name != "":
            st.write(f"""Привет, {name}!""")
            if wannasee == "Да":
                st.write("""Вот список команд, которые играли в НХЛ в 2000-2020""")
                st.dataframe(teamstat)
                st.dataframe(gamestat)

    elif language == "Deutsch":
        name = st.text_area("Wie heißt du?")
        if name != "":
            st.write(f"""Hi, {name}!""")