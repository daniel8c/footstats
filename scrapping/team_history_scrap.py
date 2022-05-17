from pandas.io.json._normalize import nested_to_record
from create_database_first_iteration import _script_to_json, create_url, create_soup,\
    connect_database, close_database, insert_row

if __name__ == '__main__':
    base_url = 'https://understat.com'
    seasons = [str(x) for x in range(2014, 2022)]
    leagues = ['EPL', 'La_Liga', 'Bundesliga', 'Serie_A', 'Ligue_1']
    try:
        connection, cursor = connect_database()
        for league in leagues:
            for season in seasons:
                url = create_url('league', league, season, base=base_url)
                print(url)
                soup = create_soup(url)
                data = _script_to_json(2, soup)

                for i in data:
                    team_id = data[i]['id']
                    title = data[i]['title']
                    for count, round_data in enumerate(data[i]['history']):
                        kolejka = count+1
                        r_data = nested_to_record(round_data, sep='_')
                        r_data['team_id'] = team_id
                        r_data['title'] = title
                        r_data['kolejka'] = kolejka
                        r_data['season'] = season
                        r_data['league'] = league
                        insert_row(connection, cursor, r_data, 'home_teamhistory')

    finally:
        close_database(connection, cursor)


