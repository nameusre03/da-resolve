import matplotlib_terminal
import numpy as np
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt

# connect to SQL database
db_path = './database.sqlite'
connection = sql.connect(db_path) # create connection object to database

query_tables = """
    SELECT
        *
    FROM sqlite_master
    WHERE type='table';
"""

#tables = pd.read_sql(query_tables, connection)
#print(tables)


query_countries = """
    SELECT
        *
    FROM Country;
"""

#countries = pd.read_sql(query_countries, connection)
#print(countries)

query_leagues = """
    SELECT
        *
    FROM League
    JOIN Country ON Country.id = League.country_id;
"""

#leagues = pd.read_sql(query_leagues, connection)
#print(leagues)


query_teams = """
    SELECT
        *
    FROM Team
    ORDER BY team_long_name
    LIMIT 10;
"""

#teams = pd.read_sql(query_teams, connection)
#print(teams)


query_detailed_matches = """
    SELECT
        Match.id, 
        Country.name AS country_name, 
        League.name AS league_name, 
        season, 
        stage, 
        date,
        HT.team_long_name AS  home_team,
        AT.team_long_name AS away_team,
        home_team_goal, 
        away_team_goal                                        
    FROM Match
    JOIN Country on Country.id = Match.country_id
    JOIN League on League.id = Match.league_id
    LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
    LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
    WHERE country_name = 'Spain'
    ORDER by date
    LIMIT 10;
"""

#detailed_matches = pd.read_sql(query_detailed_matches, connection)
#print(detailed_matches)

leages_by_season = pd.read_sql("""SELECT Country.name AS country_name, 
                                        League.name AS league_name, 
                                        season,
                                        count(distinct stage) AS number_of_stages,
                                        count(distinct HT.team_long_name) AS number_of_teams,
                                        avg(home_team_goal) AS avg_home_team_scors, 
                                        avg(away_team_goal) AS avg_away_team_goals, 
                                        avg(home_team_goal-away_team_goal) AS avg_goal_dif, 
                                        avg(home_team_goal+away_team_goal) AS avg_goals, 
                                        sum(home_team_goal+away_team_goal) AS total_goals                                       
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                JOIN League on League.id = Match.league_id
                                LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                WHERE country_name in ('Spain', 'Germany', 'France', 'Italy', 'England')
                                GROUP BY Country.name, League.name, season
                                HAVING count(distinct stage) > 10
                                ORDER BY Country.name, League.name, season DESC
                                ;""", connection)
#print(leages_by_season)

df = pd.DataFrame(index=np.sort(leages_by_season['season'].unique()), columns=leages_by_season['country_name'].unique())

df.loc[:,'Germany'] = list(leages_by_season.loc[leages_by_season['country_name']=='Germany','avg_goals'])
df.loc[:,'Spain']   = list(leages_by_season.loc[leages_by_season['country_name']=='Spain','avg_goals'])
df.loc[:,'France']   = list(leages_by_season.loc[leages_by_season['country_name']=='France','avg_goals'])
df.loc[:,'Italy']   = list(leages_by_season.loc[leages_by_season['country_name']=='Italy','avg_goals'])
df.loc[:,'England']   = list(leages_by_season.loc[leages_by_season['country_name']=='England','avg_goals'])

df.plot(figsize=(12,5),title='Average Goals per Game Over Time')

