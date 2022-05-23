from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import psycopg2
from pandas.io.json._normalize import nested_to_record


def scrapper_match_situations(soup):
    data = _script_to_json(1, soup)
    data_away = data['a']
    data_home = data['h']
    return data_away, data_home


def scrapper_match_rosters(soup):
    data = _script_to_json(2, soup)
    data_away = data['a']
    data_home = data['h']
    return data_away, data_home


def scrapper_match_result(soup):
    data = _script_to_json(1, soup)
    data = nested_to_record(data, sep='_')
    return data


def scrapper_team_history(soup):
    data = _script_to_json(2, soup)
    return data


def _script_to_json(index, soup):
    """convert scripts to json format"""

    scripts = soup.find_all('script')
    strings = scripts[index].string

    ind_start = strings.index("('") + 2
    ind_end = strings.index("')")

    json_data = strings[ind_start:ind_end]
    json_data = json_data.encode('utf-8').decode('unicode_escape')
    data = json.loads(json_data)
    return data


def insert_row(connection, cursor, row, table_name):
    column_names = str(tuple(row.keys())).replace("'", "")
    record_to_insert = list(row.values())
    postgres_insert_query = f""" INSERT INTO {table_name} {column_names} VALUES ({('%s, ' * len(record_to_insert))[:-2]})"""
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()


def create_url(*args, base, sep='/'):
    return base + '/' + sep.join(args)


def create_soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    return soup


def connect_database():
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="foot_stats")
    cursor = connection.cursor()
    return connection, cursor


def close_database(connection, cursor):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")


def match_to_database(situations_home, situations_away, roster_home, roster_away, id):
    for row_1, row_2 in zip(situations_home, situations_away):
        insert_row(connection, cursor, row_1, 'home_situationmatch')
        insert_row(connection, cursor, row_2, 'home_situationmatch')
    for row_1, row_2 in zip(list(roster_home.values()), list(roster_away.values())):
        row_1['match_id'] = str(id)
        row_2['match_id'] = str(id)
        insert_row(connection, cursor, row_1, 'home_roster')
        insert_row(connection, cursor, row_2, 'home_roster')


def match_result_to_database(match):
    insert_row(connection, cursor, match, 'home_matchresult')


if __name__ == "__main__":
    base_url = 'https://understat.com'

    # MATCH SITUATION
    index_match_situations = 1
    index_rosters = 2

    # MATCH RESULT
    seasons = [str(x) for x in range(2014, 2022)]
    leagues = ['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1']

    try:
        connection, cursor = connect_database()

        id_result_match = []
        not_result = []
        list_to_search_match = []
        for league in leagues:
            for season in seasons:
                # MATCH
                url_matches_in_season = create_url('league', league, season, base=base_url)
                print(url_matches_in_season)
                soup_matches_result = create_soup(url_matches_in_season)
                data_matches_result = scrapper_match_result(soup_matches_result)

                for match in data_matches_result:
                    match['league'] = league
                    match['league_link_id'] = league
                    match['season'] = season
                    id = match['id']
                    if id == '4238':
                        continue
                    else:
                        match_result_to_database(match)
                        if match['isResult']:
                            id_result_match.append(id)
                            url_match = create_url('match', id, base=base_url)
                            print(url_match)
                            soup_match = create_soup(url_match)

                            # situations and rosters
                            situations_away, situations_home = scrapper_match_situations(soup_match)
                            roster_away, roster_home = scrapper_match_rosters(soup_match)

                            match_to_database(situations_home, situations_away, roster_home, roster_away, id)

                            list_to_search_match.append(
                                {'id': id, 'datetime': match['datetime'], 'h_id': match['h_id'],
                                 'a_id': match['a_id']})
                        else:
                            not_result.append(id)

        # TEAM HISTORY
        for league in leagues:
            for season in seasons:
                url_matches_in_season = create_url('league', league, season, base=base_url)
                print(url_matches_in_season)
                soup_matches_result = create_soup(url_matches_in_season)

                team_history = scrapper_team_history(soup_matches_result)
                for team in team_history.values():
                    team_id = team['id']
                    title = team['title']
                    for count, hist in enumerate(team['history']):
                        round_ = count + 1
                        r_data = nested_to_record(hist, sep='_')
                        r_data['team_id'] = team_id
                        r_data['title'] = title
                        r_data['kolejka'] = round_
                        r_data['season'] = season
                        r_data['league'] = league
                        result_search = False
                        for m in list_to_search_match:
                            if m['datetime'] == r_data['date'] and (
                                    m['h_id'] == r_data['team_id'] or m['a_id'] == r_data['team_id']):
                                r_data['match_id'] = m['id']
                                result_search = True
                        if not result_search:
                            print(r_data)
                            continue
                        else:
                            insert_row(connection, cursor, r_data, 'home_teamhistory')
                break
            break
    finally:
        # closing database connection.
        if connection:
            close_database(connection, cursor)