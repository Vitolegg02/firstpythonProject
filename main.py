#let's import everything we need
import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, aes, geom_point, geom_smooth, geom_jitter
import plotly_express as px

with st.echo(code_location='below'):
    #First, let's make some functions for downloading data
    def team_abr(team_id):
        try:
            return teamstat[teamstat["team_id"] == team_id]["abbreviation"].values[0]
        except:
            return None

    def season_breaker(season):
        try:
            return(str(season)[0:4]+"-"+str(season)[4:9])
        except:
            return None

    def get_home_points(outcome):
        if outcome == "home win REG":
            return 2
        elif outcome == "home win OT":
            return 2
        elif outcome == "away win OT":
            return 1
        elif outcome == "away win REG":
            return 0
        else:
            return None

    def get_away_points(outcome):
        if outcome == "home win REG":
            return 0
        elif outcome == "home win OT":
            return 1
        elif outcome == "away win OT":
            return 2
        elif outcome == "away win REG":
            return 2
        else:
            return None

    def get_playoff_home_points(outcome):
        if outcome == "home win REG" or outcome == "home win OT":
            return 1
        elif outcome == "away win OT" or outcome == "away win REG":
            return 0
        else:
            return None

    def get_playoff_away_points(outcome):
        if outcome == "home win REG" or outcome == "home win OT":
            return 0
        elif outcome == "away win OT" or outcome == "away win REG":
            return 1
        else:
            return None

    def home_outcome(outcome):
        if outcome == "home win REG":
            return "home win REG"
        elif outcome == "home win OT":
            return "home win OT"
        elif outcome == "away win OT":
            return "home loss OT"
        elif outcome == "away win REG":
            return "home loss REG"
        else:
            return None

    def away_outcome(outcome):
        if outcome == "home win REG":
            return "away loss REG"
        elif outcome == "home win OT":
            return "away loss OT"
        elif outcome == "away win OT":
            return "away win OT"
        elif outcome == "away win REG":
            return "away win REG"
        else:
            return None

    @st.cache
    def get_teams(allow_output_mutation=True):
        return pd.read_csv(r"team_info.csv")[["team_id", "shortName", "teamName", "abbreviation"]].sort_values("team_id")
    teamstat = get_teams()

    @st.cache(allow_output_mutation=True)
    def get_games():
        gamestat = pd.read_csv(r"game.csv").drop_duplicates()[["season", "type", "away_team_id", "home_team_id", "away_goals", "home_goals", "outcome", "venue"]]
        gamestat["away_team"] = gamestat["away_team_id"].apply(team_abr)
        gamestat["home_team"] = gamestat["home_team_id"].apply(team_abr)
        gamestat["season"] = gamestat["season"].apply(season_breaker)
        gamestat["home_points"] = None
        gamestat["away_points"] = None
        return gamestat[["season", "type", "home_team", "away_team", "home_goals", "away_goals", "outcome", "home_points", "away_points"]]
    gamestat = get_games()

    @st.cache(allow_output_mutation=True)
    def get_players():
        return pd.read_csv(r"player_info.csv")
    player_info = get_players


    st.write("""
    # Hello stranger! This is my first app.
    """)

    language = st.selectbox("Please select a language / Выберите язык", ["Select", "English", "Русский", "Polska"])



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

                content = st.selectbox("What do you want to know about?", ["Select", "Teams", "Players"])
                if content == "Teams":
                    st.write("""Here is a list of teams that have been playing in the NHL in 2000-2020""")
                    st.dataframe(teamstat)

                    season = st.selectbox("Please choose a season", ["Select", "General Teams Stats", "2000-2001", "2001-2002", "2002-2003", "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020"])
                    if season == "2004-2005":
                        st.write("There was a lockout in the NHL in 2004-2005")

                    elif season == "General Teams Stats":
                        team = st.selectbox("Please chose a team you want to study", ["Select", "Total"] + list(teamstat["abbreviation"].values))
                        if team == "Total":
                            st.write("Here is a chart that shows how games ended in the NHL.")
                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            outcomes = type_gamestat.groupby("outcome").count().reset_index(level=0)[["outcome", "season"]]
                            outcomes.columns = ["outcome", "count"]
                            outcomes = outcomes[outcomes["outcome"].isin(["home win REG", "away win REG", "home win OT", "away win OT"])]
                            outcomes.sort_values("count", inplace=True)
                            fig = plt.figure()
                            plt.pie(x=outcomes["count"].values, labels=outcomes["outcome"].values,colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                            st.pyplot(fig)

                        elif team != "Select":
                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            home_gamestat = type_gamestat[type_gamestat["home_team"] == team]
                            away_gamestat = type_gamestat[type_gamestat["away_team"] == team]
                            home_gamestat["home outcome"] = home_gamestat["outcome"].apply(home_outcome)
                            away_gamestat["away outcome"] = away_gamestat["outcome"].apply(away_outcome)
                            home_totalstat = home_gamestat.groupby("home outcome").count().reset_index(level=0)[["home outcome", "season"]]
                            away_totalstat = away_gamestat.groupby("away outcome").count().reset_index(level=0)[["away outcome", "season"]]
                            home_totalstat.columns = ["outcome", "count"]
                            away_totalstat.columns = ["outcome", "count"]
                            home_totalstat.sort_values("count", inplace=True)
                            away_totalstat.sort_values("count", inplace=True)
                            totalstat = pd.concat([home_totalstat, away_totalstat]).sort_values("count")

                            st.write(f"Let's take a look at how {team} performed over time.")
                            location = st.selectbox("Which location are you interested in?", ["Select", "Total", "Home", "Away"])
                            if location == "Total":
                                fig = plt.figure()
                                plt.pie(x=totalstat["count"].values, labels=totalstat["outcome"].values, colors = ["mistyrose", "pink", "lightcoral", "indianred", "firebrick", "brown", "darkred", "maroon"], autopct='%.2f')
                                st.pyplot(fig)
                            elif location == "Home":
                                fig = plt.figure()
                                plt.pie(x=home_totalstat["count"].values, labels=home_totalstat["outcome"].values, colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                st.pyplot(fig)
                            elif location == "Away":
                                fig = plt.figure()
                                plt.pie(x=away_totalstat["count"].values, labels=away_totalstat["outcome"].values, colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                st.pyplot(fig)

                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_home_points)
                            type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_away_points)
                            home_points = type_gamestat[type_gamestat["home_team"] == team][["season", "home_team", "home_points"]].groupby(["season", "home_team"]).sum()
                            home_points.columns = ["points"]
                            away_points = type_gamestat[type_gamestat["away_team"] == team][["season", "away_team", "away_points"]].groupby(["season", "away_team"]).sum()
                            away_points.columns = ["points"]
                            total_points = home_points + away_points
                            total_points.reset_index(level=0, inplace=True)

                            st.write(f"Let's also take a look at how {team} has developed over the years, and how many points it had each season")
                            figure = px.line(data_frame=total_points, x="season", y="points", range_y=[0,130])
                            st.plotly_chart(figure)




                    elif season != "Select":
                        season_gamestat = gamestat[gamestat["season"] == season]
                        type = st.selectbox("Please choose also if you want to look at regular season stats, or at the Playoffs", ["Select", "Regular", "Playoff"])
                        if type == "Regular":
                            type_gamestat = season_gamestat[season_gamestat["type"] == "R"]
                            type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_home_points)
                            type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_away_points)
                            home_points = type_gamestat[["home_team", "home_points"]].groupby("home_team").sum().sort_values("home_points", ascending = False)
                            home_points.columns = ["points"]
                            away_points = type_gamestat[["away_team", "away_points"]].groupby("away_team").sum().sort_values("away_points", ascending=False)
                            away_points.columns = ["points"]
                            total_points = (home_points + away_points).sort_values("points", ascending = False)
                            total_points.reset_index(level=0, inplace=True)
                            total_points.columns = ["team", "points"]
                            home_points.reset_index(level=0, inplace=True)
                            home_points.columns = ["team", "points"]
                            away_points.reset_index(level=0, inplace=True)
                            away_points.columns = ["team", "points"]

                            where = st.selectbox("Which table do you want to see?",["Select", "Total", "Home", "Away"])

                            if where == "Total":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points",y="team",data=total_points,palette=reversed(sns.color_palette('Blues_d',n_colors=len(total_points))))
                                st.pyplot(fig)
                            elif where == "Home":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points", y="team", data=home_points, palette=reversed(sns.color_palette('Blues_d', n_colors=len(total_points))))
                                st.pyplot(fig)
                            elif where == "Away":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points", y="team", data=away_points, palette=reversed(sns.color_palette('Blues_d', n_colors=len(total_points))))
                                st.pyplot(fig)

                            wannateams = st.selectbox("Do you also want to learn something about the teams?", ["Select", "Yes", "No"])
                            if wannateams == "Yes":
                                team = st.selectbox("Which team are you interested in?", ["Select", "Total"] + list(teamstat["abbreviation"].values))
                                if team == "Total":
                                    st.write(f"Here is a chart that shows how games ended in the NHL in {season}.")
                                    outcomes = type_gamestat.groupby("outcome").count().reset_index(level=0)[["outcome", "season"]]
                                    outcomes.columns = ["outcome", "count"]
                                    outcomes = outcomes[outcomes["outcome"].isin(["home win REG", "away win REG", "home win OT", "away win OT"])]
                                    outcomes.sort_values("count", inplace=True)
                                    fig = plt.figure()
                                    plt.pie(x=outcomes["count"].values, labels=outcomes["outcome"].values,colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                    st.pyplot(fig)

                                elif team != "Select":
                                    home_gamestat = type_gamestat[type_gamestat["home_team"] == team]
                                    away_gamestat = type_gamestat[type_gamestat["away_team"] == team]
                                    home_gamestat["home outcome"] = home_gamestat["outcome"].apply(home_outcome)
                                    away_gamestat["away outcome"] = away_gamestat["outcome"].apply(away_outcome)
                                    home_totalstat = home_gamestat.groupby("home outcome").count().reset_index(level=0)[["home outcome", "season"]]
                                    away_totalstat = away_gamestat.groupby("away outcome").count().reset_index(level=0)[["away outcome", "season"]]
                                    home_totalstat.columns = ["outcome", "count"]
                                    away_totalstat.columns = ["outcome", "count"]
                                    home_totalstat.sort_values("count", inplace=True)
                                    away_totalstat.sort_values("count", inplace=True)
                                    totalstat = pd.concat([home_totalstat, away_totalstat]).sort_values("count")

                                    st.write(f"Let's take a look at how {team} performed in {season}.")
                                    location = st.selectbox("Which location are you interested in?", ["Select", "Total", "Home", "Away"])
                                    if location == "Total":
                                        fig = plt.figure()
                                        plt.pie(x=totalstat["count"].values, labels=totalstat["outcome"].values, colors=["mistyrose", "pink", "lightcoral", "indianred", "firebrick", "brown", "darkred", "maroon"], autopct='%.2f')
                                        st.pyplot(fig)
                                    elif location == "Home":
                                        fig = plt.figure()
                                        plt.pie(x=home_totalstat["count"].values, labels=home_totalstat["outcome"].values, colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                        st.pyplot(fig)
                                    elif location == "Away":
                                        fig = plt.figure()
                                        plt.pie(x=away_totalstat["count"].values, labels=away_totalstat["outcome"].values, colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                        st.pyplot(fig)

                        elif type == "Playoff":
                            if season in ["2000-2001", "2001-2002", "2002-2003", "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009", "2009-2010"]:
                                st.write("There is no playoff data for 2000-2010")
                            else:
                                type_gamestat = season_gamestat[season_gamestat["type"] == "P"]
                                type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_playoff_home_points)
                                type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_playoff_away_points)
                                home_points = type_gamestat[["home_team", "home_points"]].groupby("home_team").sum().sort_values("home_points", ascending=False)
                                home_points.columns = ["wins"]
                                away_points = type_gamestat[["away_team", "away_points"]].groupby("away_team").sum().sort_values("away_points", ascending=False)
                                away_points.columns = ["wins"]
                                total_points = (home_points + away_points).sort_values("wins", ascending=False)
                                total_points.reset_index(level=0,inplace=True)
                                total_points.columns = ["team", "wins"]
                                st.write("Unfortunately, I did not have the time to complete this section with a cool animation, but you can take a look at the table, which will show you the Stanley Cup winner.")
                                st.dataframe(total_points)
                elif content == "Players":
                    st.write("Sorry, there wasn't enough time, I did not manage to do this section yet.")



    elif language == "Русский":
        name = st.text_area("Привет, как тебя зовут?")
        if name == "Анфиса":
            st.write("""Привет, Анфиса! Рад тебя видеть! Говорят, ты самая красивая девочка на свете.""")

        elif name != "":
            st.write(f"""Привет, {name}!""")
            wannasee = st.selectbox("Хочешь, расскажу немного о хоккее?", ["Выбрать", "Да", "Нет"])
            if wannasee == "Да":

                content = st.selectbox("О чем ты хочешь узнать?", ["Выбрать", "Команды", "Игроки"])
                if content == "Команды":
                    st.write("""Вот список команд, которые выступали в НХЛ в 2000-2020""")
                    st.dataframe(teamstat)

                    season = st.selectbox("Выберите сезон, который вас интересует",
                                          ["Выбрать", "Сквозная статистика по командам", "2000-2001", "2001-2002", "2002-2003",
                                           "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008", "2008-2009",
                                           "2009-2010", "2010-2011", "2011-2012", "2011-2012", "2012-2013", "2013-2014",
                                           "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019",
                                           "2019-2020"])
                    if season == "2004-2005":
                        st.write("В 2004-2005 годах в НХЛ происходил локдаун")

                    elif season == "Сквозная статистика по командам":
                        team = st.selectbox("Пожалуйста, выберите команду, которая вам интересна",
                                            ["Выбрать", "Сводка"] + list(teamstat["abbreviation"].values))
                        if team == "Сводка":
                            st.write("Посмотрите, как заканчивались игры в НХЛ")
                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            outcomes = type_gamestat.groupby("outcome").count().reset_index(level=0)[
                                ["outcome", "season"]]
                            outcomes.columns = ["outcome", "count"]
                            outcomes = outcomes[outcomes["outcome"].isin(
                                ["home win REG", "away win REG", "home win OT", "away win OT"])]
                            outcomes.sort_values("count", inplace=True)
                            fig = plt.figure()
                            plt.pie(x=outcomes["count"].values, labels=outcomes["outcome"].values,
                                    colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                            st.pyplot(fig)

                        elif team != "Выбрать":
                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            home_gamestat = type_gamestat[type_gamestat["home_team"] == team]
                            away_gamestat = type_gamestat[type_gamestat["away_team"] == team]
                            home_gamestat["home outcome"] = home_gamestat["outcome"].apply(home_outcome)
                            away_gamestat["away outcome"] = away_gamestat["outcome"].apply(away_outcome)
                            home_totalstat = home_gamestat.groupby("home outcome").count().reset_index(level=0)[
                                ["home outcome", "season"]]
                            away_totalstat = away_gamestat.groupby("away outcome").count().reset_index(level=0)[
                                ["away outcome", "season"]]
                            home_totalstat.columns = ["outcome", "count"]
                            away_totalstat.columns = ["outcome", "count"]
                            home_totalstat.sort_values("count", inplace=True)
                            away_totalstat.sort_values("count", inplace=True)
                            totalstat = pd.concat([home_totalstat, away_totalstat]).sort_values("count")

                            st.write(f"Давайте посмотрим как {team} выступал в течение последних лет.")
                            location = st.selectbox("Вас интересует как команда играла",
                                                    ["Выбрать", "Везде", "Дома", "В гостях"])
                            if location == "Везде":
                                fig = plt.figure()
                                plt.pie(x=totalstat["count"].values, labels=totalstat["outcome"].values,
                                        colors=["mistyrose", "pink", "lightcoral", "indianred", "firebrick", "brown",
                                                "darkred", "maroon"], autopct='%.2f')
                                st.pyplot(fig)
                            elif location == "Дома":
                                fig = plt.figure()
                                plt.pie(x=home_totalstat["count"].values, labels=home_totalstat["outcome"].values,
                                        colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                st.pyplot(fig)
                            elif location == "В гостях":
                                fig = plt.figure()
                                plt.pie(x=away_totalstat["count"].values, labels=away_totalstat["outcome"].values,
                                        colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                st.pyplot(fig)

                            type_gamestat = gamestat[gamestat["type"] == "R"]
                            type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_home_points)
                            type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_away_points)
                            home_points = type_gamestat[type_gamestat["home_team"] == team][
                                ["season", "home_team", "home_points"]].groupby(["season", "home_team"]).sum()
                            home_points.columns = ["points"]
                            away_points = type_gamestat[type_gamestat["away_team"] == team][
                                ["season", "away_team", "away_points"]].groupby(["season", "away_team"]).sum()
                            away_points.columns = ["points"]
                            total_points = home_points + away_points
                            total_points.reset_index(level=0, inplace=True)

                            st.write(
                                f"Давайте также посмотрим как {team} развивалась со временем, и посмотрим, сколько очков она набрала в каждом сезоне.")
                            figure = px.line(data_frame=total_points, x="season", y="points", range_y=[0, 130])
                            st.plotly_chart(figure)




                    elif season != "Выбрать":
                        season_gamestat = gamestat[gamestat["season"] == season]
                        type = st.selectbox(
                            "Вас интересуют данные по Регулярке, или по Плей-Оффам?",
                            ["Выбрать", "Регулярка", "Плей-Офф"])
                        if type == "Регулярка":
                            type_gamestat = season_gamestat[season_gamestat["type"] == "R"]
                            type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_home_points)
                            type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_away_points)
                            home_points = type_gamestat[["home_team", "home_points"]].groupby(
                                "home_team").sum().sort_values("home_points", ascending=False)
                            home_points.columns = ["points"]
                            away_points = type_gamestat[["away_team", "away_points"]].groupby(
                                "away_team").sum().sort_values("away_points", ascending=False)
                            away_points.columns = ["points"]
                            total_points = (home_points + away_points).sort_values("points", ascending=False)
                            total_points.reset_index(level=0, inplace=True)
                            total_points.columns = ["team", "points"]
                            home_points.reset_index(level=0, inplace=True)
                            home_points.columns = ["team", "points"]
                            away_points.reset_index(level=0, inplace=True)
                            away_points.columns = ["team", "points"]

                            where = st.selectbox("Какая таблица вас интересует?", ["Выбрать", "Везде", "Дома", "В гостях"])

                            if where == "Везде":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points", y="team", data=total_points,
                                            palette=reversed(sns.color_palette('Blues_d', n_colors=len(total_points))))
                                st.pyplot(fig)
                            elif where == "Дома":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points", y="team", data=home_points,
                                            palette=reversed(sns.color_palette('Blues_d', n_colors=len(total_points))))
                                st.pyplot(fig)
                            elif where == "В гостях":
                                fig, ax = plt.subplots()
                                sns.barplot(x="points", y="team", data=away_points,
                                            palette=reversed(sns.color_palette('Blues_d', n_colors=len(total_points))))
                                st.pyplot(fig)

                            wannateams = st.selectbox("Хотите ли вы узнать еще что-то о командах?",
                                                      ["Выбрать", "Да", "Нет"])
                            if wannateams == "Да":
                                team = st.selectbox("Какая команда вас интересует?",
                                                    ["Выбрать", "Все"] + list(teamstat["abbreviation"].values))
                                if team == "Все":
                                    st.write(f"Here is a chart that shows how games ended in the NHL in {season}.")
                                    outcomes = type_gamestat.groupby("outcome").count().reset_index(level=0)[
                                        ["outcome", "season"]]
                                    outcomes.columns = ["outcome", "count"]
                                    outcomes = outcomes[outcomes["outcome"].isin(
                                        ["home win REG", "away win REG", "home win OT", "away win OT"])]
                                    outcomes.sort_values("count", inplace=True)
                                    fig = plt.figure()
                                    plt.pie(x=outcomes["count"].values, labels=outcomes["outcome"].values,
                                            colors=["royalblue", "blue", "darkblue", "midnightblue"], autopct='%.2f')
                                    st.pyplot(fig)

                                elif team != "Выбрать":
                                    home_gamestat = type_gamestat[type_gamestat["home_team"] == team]
                                    away_gamestat = type_gamestat[type_gamestat["away_team"] == team]
                                    home_gamestat["home outcome"] = home_gamestat["outcome"].apply(home_outcome)
                                    away_gamestat["away outcome"] = away_gamestat["outcome"].apply(away_outcome)
                                    home_totalstat = home_gamestat.groupby("home outcome").count().reset_index(level=0)[
                                        ["home outcome", "season"]]
                                    away_totalstat = away_gamestat.groupby("away outcome").count().reset_index(level=0)[
                                        ["away outcome", "season"]]
                                    home_totalstat.columns = ["outcome", "count"]
                                    away_totalstat.columns = ["outcome", "count"]
                                    home_totalstat.sort_values("count", inplace=True)
                                    away_totalstat.sort_values("count", inplace=True)
                                    totalstat = pd.concat([home_totalstat, away_totalstat]).sort_values("count")

                                    st.write(f"Давайте посмотрим, как {team} выступила в {season} сезоне.")
                                    location = st.selectbox("Выберите локацию",
                                                            ["Выбрать", "Везде", "Дома", "В гостях"])
                                    if location == "Везде":
                                        fig = plt.figure()
                                        plt.pie(x=totalstat["count"].values, labels=totalstat["outcome"].values,
                                                colors=["mistyrose", "pink", "lightcoral", "indianred", "firebrick",
                                                        "brown", "darkred", "maroon"], autopct='%.2f')
                                        st.pyplot(fig)
                                    elif location == "Дома":
                                        fig = plt.figure()
                                        plt.pie(x=home_totalstat["count"].values,
                                                labels=home_totalstat["outcome"].values,
                                                colors=["royalblue", "blue", "darkblue", "midnightblue"],
                                                autopct='%.2f')
                                        st.pyplot(fig)
                                    elif location == "В гостях":
                                        fig = plt.figure()
                                        plt.pie(x=away_totalstat["count"].values,
                                                labels=away_totalstat["outcome"].values,
                                                colors=["royalblue", "blue", "darkblue", "midnightblue"],
                                                autopct='%.2f')
                                        st.pyplot(fig)

                        elif type == "Плей-Офф":
                            if season in ["2000-2001", "2001-2002", "2002-2003", "2003-2004", "2004-2005", "2005-2006",
                                          "2006-2007", "2007-2008", "2008-2009", "2009-2010"]:
                                st.write("К сожалению, нет данных по плей-оффам 2000-2010")
                            else:
                                type_gamestat = season_gamestat[season_gamestat["type"] == "P"]
                                type_gamestat["home_points"] = type_gamestat["outcome"].apply(get_playoff_home_points)
                                type_gamestat["away_points"] = type_gamestat["outcome"].apply(get_playoff_away_points)
                                home_points = type_gamestat[["home_team", "home_points"]].groupby(
                                    "home_team").sum().sort_values("home_points", ascending=False)
                                home_points.columns = ["wins"]
                                away_points = type_gamestat[["away_team", "away_points"]].groupby(
                                    "away_team").sum().sort_values("away_points", ascending=False)
                                away_points.columns = ["wins"]
                                total_points = (home_points + away_points).sort_values("wins", ascending=False)
                                total_points.reset_index(level=0, inplace=True)
                                total_points.columns = ["team", "wins"]
                                st.write(
                                    "К сожалению, я не успел сделать классную анимацию в эту секцию, так что вы можете просто посмотреть на таблицу, которая покажет вам победителя Кубка Стенли.")
                                st.dataframe(total_points)
                elif content == "Игроки":
                    st.write("Извините, к сожалению у меня не было достаточно времени, чтобы завершить этот этап.")