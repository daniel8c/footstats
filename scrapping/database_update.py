from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import psycopg2
from pandas.io.json._normalize import nested_to_record


def scrapper_match_situation(index):
    data = _script_to_json(index)
    data_away = data['a']
    data_home = data['h']
    return data_away, data_home


def scrapper_match_result():
    data = _script_to_json(1)
    data = nested_to_record(data, sep='_')
    return data


def _script_to_json(index):
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
    # print(table_name, row)
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


def situation_to_database():
    data_away, data_home = scrapper_match_situation(index_match_situations)
    rosters_away, rosters_home = scrapper_match_situation(index_rosters)
    for row_1, row_2 in zip(data_home, data_away):
        insert_row(connection, cursor, row_1, 'home_situationmatch')
        insert_row(connection, cursor, row_2, 'home_situationmatch')
    for row_1, row_2 in zip(list(rosters_home.values()), list(rosters_away.values())):
        row_1['match_id'] = str(id)
        row_2['match_id'] = str(id)
        insert_row(connection, cursor, row_1, 'home_roster')
        insert_row(connection, cursor, row_2, 'home_roster')


def match_to_database():
    insert_row(connection, cursor, match, 'home_matchresult')

def update_row(connection, cursor, row, table_name):
    column_names = str(tuple(row.keys())).replace("'", "")
    record_to_insert = list(row.values())
    postgres_insert_query = f""" UPDATE {table_name} SET {column_names} = ({('%s, ' * len(record_to_insert))[:-2]}) WHERE id = {int(row['id'])}"""
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()




if __name__ == "__main__":
    # MATCH SITUATION
    base_url = 'https://understat.com'
    index_match_situations = 1
    index_rosters = 2

    seasons = ['2021']
    leagues = ['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1']

    result = []
    not_result = []

    # wyciąganie ze strony match_id
    for league in leagues:
        for season in seasons:
            url = create_url('league', league, season, base=base_url)
            print(url)
            soup = create_soup(url)

            data = scrapper_match_result()
            for match in data:
                if match['id'] == '4238':
                    continue
                else:
                    if match['isResult']:
                        result.append(match['id'])
                    else:
                        not_result.append(match['id'])

    # porównanie z ostatnią iteracją
    with open(r'C:\footstats\log\not_result.txt', 'r') as f_not_result_last:
        not_result_last = [x.rstrip() for x in f_not_result_last.readlines()]

    id_result_match = list(set(result) & set(not_result_last))
    print(id_result_match)

    with open(r'C:\footstats\log\result.txt', 'w') as f_result_now:
        for id in result:
            f_result_now.write(id + '\n')



    # update database
    if id_result_match:
        try:
            connection, cursor = connect_database()

            for league in leagues:
                for season in seasons:
                    url = create_url('league', league, season, base=base_url)
                    print(url)
                    soup = create_soup(url)

                    data = scrapper_match_result()

                    for match in data:
                        if match['id'] in id_result_match:
                            match['league'] = league
                            match['season'] = season
                            update_row(connection, cursor, match, 'home_matchresult')

            for id in id_result_match:
                url = create_url('match', id, base=base_url)
                print(url)
                soup = create_soup(url)

                situation_to_database()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into mobile table", error)

        finally:
            # closing database connection.
            if connection:
                close_database(connection, cursor)

    with open(r'C:\footstats\log\not_result.txt', 'w') as f_not_result_now:
        for id in not_result:
            f_not_result_now.write(id + '\n')
