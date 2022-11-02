"""Read participant round selection data from a data files"""
import re
import pandas as pd
from scripts import DataFile, DataBaseOperations
from scripts import nhl_teams
from scripts.nhl_teams import shorten_team_name as stn

class Selections(DataFile):
    """Class for gathering and processing information about a playoff round"""

    def __init__(
            self,
            year,
            playoff_round,
            selections_directory=None,
            keep_results=False,
            **kwargs
        ):
        super().__init__(year=year, playoff_round=playoff_round, directory=selections_directory)
        self._database = DataBaseOperations(**kwargs)
        with self.database as db:
            self._in_database = db.year_round_in_database(year, playoff_round)
        self._load_selections(keep_results=keep_results)

    @property
    def selections(self):
        """All selections for the playoff round"""
        return self._selections

    @property
    def individuals(self):
        """The individuals in the playoff round"""
        return sorted(list(set(self.selections.index.get_level_values('Individual'))))

    @property
    def database(self):
        """The database"""
        return self._database

    @property
    def series(self):
        """Return the teams in each series in each conference"""

        if self.playoff_round not in [1,2,3,4]:
            raise ValueError('The series method does not apply for the Champions playoff round')

        if self._in_database:
            return self._conference_series_from_database()
        else:
            return self._conference_series_from_file()

    def _load_selections(self, **kwargs):
        """Load the selections from database or raw source file"""

        if self._in_database:
            if self.playoff_round in [1,2,3,4]:
                self._selections = self._load_playoff_round_selections_from_database()
            elif self.playoff_round == 'Champions':
                self._selections = self._load_champions_selections_from_database()
        else:
            print(f'Round data for {self.playoff_round} in {self.year} is not '\
                    f'in the database with path\n {self.database.path}')
            if self.playoff_round in [1,2,3,4]:
                self._selections = self._load_playoff_round_selections_from_file(**kwargs)
            elif self.playoff_round == 'Champions':
                self._selections = self._load_champions_selections_from_file(**kwargs)

    def _load_playoff_round_selections_from_file(self, keep_results=False):
        """Return the playoff round selections from the raw source file"""

        data = pd.read_csv(self.source_file, sep=',')
        series = [col for col in data.columns
                        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", col))]
        data.rename(columns={'Name:': 'Individual'}, inplace=True)
        data.rename(columns=dict(list(zip(series, [f'{ser}Team' for ser in series]))), inplace=True)
        if not keep_results:
            data = data[data.Individual != 'Results']
        data.drop(columns=['Timestamp'], inplace=True)
        if self.playoff_round == 1:
            # drop champions data
            data.drop(columns=data.columns[17:], inplace=True)

        def get_conference(series: str):
            """The conference for the teams in the series"""
            return None if self.playoff_round == 4 else \
                nhl_teams.conference(series[:3], self.year)

        selections = pd.wide_to_long(data,
            stubnames=series,
            i='Individual',
            j='Selections',
            suffix='\\D+').stack().unstack(-2)

        # add conference to index
        conf_index = [get_conference(a_series) for a_series in selections.index.get_level_values(1)]
        selections.set_index(pd.Index(conf_index), append=True, inplace=True)
        selections.index.names = ['Individual', 'Series', 'Conference']
        df = selections.reorder_levels(['Individual', 'Conference', 'Series'])

        df.rename(columns={' series length:': 'Duration'}, inplace=True)
        df.loc[:,'Duration'] = df.loc[:,'Duration'].str[0].astype(int)
        selections = df[['Team', 'Duration']]
        selections.sort_index(level=[0,1], sort_remaining=False, inplace=True)

        if "PlayerSelection" not in selections.columns:
            selections.insert(2, "Player", [None]*len(selections))

        return selections

    def _load_champions_selections_from_file(self, keep_results=False):
        """Return the champions selections from the raw source file"""

        def select_conference_team(row, conference):
            """Return the team in the dataframe row for a particular conference"""

            champions_headers = [
                'Who will win the Stanley Cup?',
                'Who will be the Stanley Cup runner-up?'
            ]

            if conference != 'Stanley Cup':
                teams = row[champions_headers].values.tolist()
                return teams[0] \
                    if nhl_teams.conference(teams[0], self.year) == conference \
                    else teams[1]
            else:
                return row['Who will win the Stanley Cup?']

        data = pd.read_csv(self.source_file, sep=',')
        data.rename(columns={'Name:': 'Individual'}, inplace=True)
        data.index = data['Individual']
        if not keep_results:
            data.drop(index='Results', inplace=True)
        data.columns.name = 'Selections'

        champions_headers = ['East', 'West', 'Stanley Cup']
        for conference in champions_headers:
            data[conference] = data.apply(
                            lambda row, conf=conference: select_conference_team(row, conf), axis=1)

        if "Duration" not in data.columns:
            data.insert(len(data.columns), "Duration", [None]*len(data))

        return data[champions_headers+['Duration']]

    def _load_playoff_round_selections_from_database(self):
        """Return the playoff round selections from the database"""

        with self.database as db:
            data = db.get_all_round_selections(self.year, self.playoff_round)

        num_individuals = len(data.index.unique())
        series_list = [subval for values in self.series.values() for subval in values]
        data.drop(columns=['SeriesNumber'], inplace=True)
        data.set_index('Conference', append=True, inplace=True)
        data.set_index(pd.Index(series_list*num_individuals), append=True, inplace=True)
        data.index.names = ['Individual', 'Conference', 'Series']
        data.columns.name = 'Selections'

        new_names = {
            'TeamSelection': 'Team',
            'GameSelection': 'Duration',
            'PlayerSelection': 'Player',
        }
        data.rename(columns=new_names, inplace=True)
        return data

    def _load_champions_selections_from_database(self):
        """Return the Champions selections from the database"""

        with self.database as db:
            data = db.get_stanley_cup_selections(self.year)

        data.columns.name = 'Selections'
        new_names = {
            'EastSelection': 'East',
            'WestSelection': 'West',
            'StanleyCupSelection': 'Stanley Cup',
            'GameSelection': 'Duration',
        }
        data.rename(columns=new_names, inplace=True)
        return data

    def _conference_series_from_file(self):
        """Turn a list of series into a dictionary of series in each conference"""

        data = pd.read_csv(self.source_file, sep=',')
        # abbreviated series name
        series = [col for col in data.columns
                        if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", col))]
        conference_list = self._conference_list()

        def correct_conference(series: str, conference: str):
            """Boolean for correct conference of the teams"""
            return True if self.playoff_round == 4 else \
                nhl_teams.conference(series[:3], self.year) == conference \
                and nhl_teams.conference(series[-3:], self.year) == conference

        return {conf:
            [a_series for a_series in series if correct_conference(a_series, conf)]
            for conf in conference_list
        }

    def _conference_series_from_database(self):
        """Turn a list of series into a dictionary of series in each conference"""

        with self.database as db:
            series_table = db.get_all_series_in_round(self.year, self.playoff_round)
        num_series = series_table['SeriesNumber'].max()
        conference_list = self._conference_list()

        def series_name(conference, series_number):
            """Get the series name for a series number in a conference
            from the pandas table from the database"""

            conference = conference if conference is None else f'"{conference}"'
            return '-'.join(
                list(map(stn, series_table.query(
                    f"Conference in [{conference}] and SeriesNumber=={series_number}"
                )
                [['TeamHigherSeed','TeamLowerSeed']].values[0]))
            )

        return {conf:
            [series_name(conf, num) for num in range(1, num_series+1)]
            for conf in conference_list
        }

    def _conference_list(self):
        """List the conferences in the current playoff round"""

        if self.playoff_round == 4:
            return [None]
        elif self.playoff_round in [1,2,3]:
            return ['East', 'West']
