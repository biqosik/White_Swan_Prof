from soccerapi.api import Api888Sport
from sqlalchemy import create_engine

import pandas as pd

class main():
    def __init__(self):
        df_together = self.get_data()
        database = self.to_database(df_together)
        self.option_for_test(database)

    def get_data(self):
        api = Api888Sport() # Using API from Github
        url_england = 'https://www.888sport.com/#/filter/football/england/'
        odds_england = api.odds(url_england)
        url_italy = 'https://www.888sport.com/#/filter/football/italy/'
        odds_italy = api.odds(url_italy)
        url_germany = 'https://www.888sport.com/#/filter/football/germany/'
        odds_germany = api.odds(url_germany)
        odd_together = odds_italy + odds_england + odds_germany
        df_together = pd.json_normalize(odd_together)
        # df_together.to_csv('database.csv', index=False) - DATA FRAME TO CSV
        return df_together

    def to_database(self, df_together):
        engine = create_engine('sqlite://', echo=False)
        tempkey = df_together.keys()
        for x in tempkey[6:13]:
            df_together.pop(x)
        with engine.begin() as connection:
             df_together.to_sql('bettingdata', con=connection, if_exists='append')
        return engine.execute("SELECT * FROM bettingdata").fetchall()

    def option_for_test(self, database):
        global position
        while True:
            a = input(('Would you like to have the best bet available soon? Yes/No '))
            if a == 'Yes' or a == 'yes':
                temp_dict = (100000, 10000, 10000)
                for x, y in enumerate(database):
                    checking =y[4:8]
                    if checking < temp_dict:
                        temp_dict = checking
                        position = x
                print("You should aim to bet the match on date %s between %s and %s" % (database[position][1], database[position][2], database[position][3]))
                return True
            else:
                return False




if __name__ == '__main__':
    main()
