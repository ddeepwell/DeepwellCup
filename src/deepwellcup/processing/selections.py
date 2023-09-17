"""Read participant round selection data from a data files"""
import re
import math
import warnings
import pandas as pd
from .database import DataBaseOperations
from .nhl_teams import (
    conference as team_conference,
    shorten_team_name as stn,
    lengthen_team_name as ltn,
    team_of_player,
)
from . import files, utils
from .utils import DataStores


class Selections():
    """Class for gathering and processing information about a playoff round"""

    def __init__(
        self,
        year,
        playoff_round,
        keep_results=False,
        use_database_first=True,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._datastores = datastores
        self._database = DataBaseOperations(datastores.database)
        self._use_database_first = use_database_first
        with self.database as db:
            if playoff_round in utils.played_rounds(self.year):
                self.in_database = db.year_round_in_database(year, playoff_round)
            else:
                self.in_database = db.champions_round_in_database(year)
            self._results_in_database = db.year_round_results_in_database(year, playoff_round)
        self._selections_file = files.selections_file(
            year=self.year,
            selection_round=self.playoff_round,
            directory=self._datastores.raw_data_directory,
        )
        self._selections_overtime = None
        self._preferences = None
        self._monikers = None
        self._load_selections(keep_results)

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def selections(self):
        """All selections for the playoff round"""
        return self._selections

    @property
    def individuals(self):
        """The individuals in the playoff round"""
        return sorted(set(self.selections.index.get_level_values('Individual')))

    @property
    def monikers(self):
        """The monikers for individuals in the playoff round"""
        return self._monikers

    @property
    def database(self):
        """The database"""
        return self._database

    @property
    def use_database_first(self):
        """Try to use the database first before the CSV"""
        return self._use_database_first

    def _raise_error_if_champions_round(self):
        if self.playoff_round == 'Champions':
            raise ValueError('The playoff round must not be the Champions round')

    @property
    def series(self):
        """Return the teams in each series in each conference"""
        self._raise_error_if_champions_round()
        if self.in_database and self.use_database_first:
            return self._conference_series_from_database()
        else:
            return self._conference_series_from_file()

    @property
    def players_selected(self):
        """Return a boolean indicating if players where selected"""
        return 'Player' in self.selections.columns

    @property
    def players(self):
        """Return the players in each series in each conference"""
        self._raise_error_if_champions_round()
        if not self.players_selected:
            raise ValueError(
                "The 'players' category doesn't exist in "
                f"round {self.playoff_round} in {self.year}"
            )
        return {conference: [self._players_in_series(series) for series in series_teams]
                for conference, series_teams in self.series.items()}

    @property
    def overtime_selected(self):
        """Return a boolean indicating if overtime was selected"""
        return self._selections_overtime is not None

    @property
    def selections_overtime(self):
        """Return the overtime selected"""
        self._raise_error_if_champions_round()
        return self._selections_overtime

    @property
    def preferences_selected(self):
        """Return a boolean indicating if preferences were selected"""
        return self._preferences is not None

    @property
    def preferences(self):
        """Return the selected preferences"""
        self._raise_error_if_champions_round()
        return self._preferences

    def _players_in_series(self, series):
        """Return the players in the series"""
        players = list(set(self.selections['Player']))
        teams_in_series = [ltn(team) for team in series.split('-')]
        players_to_keep = [
            player for player in players
            if team_of_player(player) in teams_in_series
        ]
        if team_of_player(players_to_keep[0]) != teams_in_series[0]:
            players_to_keep.reverse()
        return players_to_keep

    def _load_selections(self, keep_results=False):
        """Load the selections from database or raw file"""
        if (
            self.in_database
            and self.use_database_first
            and (
                not keep_results
                or self._results_in_database
            )
        ):
            if self.playoff_round in utils.played_rounds(self.year):
                with self.database as db:
                    self._selections_overtime = db.get_overtime_selections(
                        self.year, self.playoff_round
                    )
                    self._preferences = db.get_all_round_preferences(self.year, self.playoff_round)
                    self._monikers = db.get_all_round_monikers(self.year, self.playoff_round)
                self._selections = self._load_playoff_round_selections_from_database()
            elif self.playoff_round == 'Champions':
                self._selections = self._load_champions_selections_from_database()
        else:
            print(
                f'Round data for {self.playoff_round} in {self.year} is not '
                f'in the database with path\n {self.database.path}'
            )
            if self.playoff_round in utils.played_rounds(self.year):
                self._load_monikers_from_file()
                self._load_overtime_selections_from_file()
                self._load_preferences_from_file()
                self._selections = self._load_playoff_round_selections_from_file(keep_results)
            elif self.playoff_round == 'Champions':
                self._selections = self._load_champions_selections_from_file(keep_results)

    def _read_data_file(self):
        """Read selections from selections file"""
        data = pd.read_csv(
            self._selections_file,
            sep=',',
            converters={
                'Name:': str.strip,
                'Moniker': str.strip,
            }
        )
        return data.rename(columns={'Name:': 'Individual'})

    def _load_monikers_from_file(self):
        """Extract monikers from file"""
        data = self._read_data_file()
        if 'Moniker' in data.columns:
            self._monikers = (
                data[['Individual', 'Moniker']]
                .set_index('Individual')
                .drop(labels='Results', axis='index')
                .squeeze()
                .sort_index()
                # .replace(to_replace="", value=None)
                .to_dict()
            )

    def _load_overtime_selections_from_file(self):
        """Extract overtime selections from file"""
        data = self._read_data_file()
        if 'How many overtime games will occur this round?' in data.columns:
            self._selections_overtime = (
                data
                .rename(
                    columns={'How many overtime games will occur this round?': 'Overtime'}
                )
                [['Individual', 'Overtime']]
                .set_index('Individual')
                .squeeze()
                .sort_index()
                .astype('str')
            )

    def _load_preferences_from_file(self):
        """Extract team preferences from file"""
        data = self._read_data_file()
        if 'Favourite team:' in data.columns and 'Current team cheering for:' in data.columns:
            self._preferences = (
                data.rename(
                    columns={
                        'Favourite team:': 'Favourite team',
                        'Current team cheering for:': 'Cheering team',
                    }
                )
                [['Individual', 'Favourite team', 'Cheering team']]
                .set_index('Individual')
                .drop(index='Results')
                .squeeze()
                .sort_index()
                .astype('str')
            )

    def _load_playoff_round_selections_from_file(self, keep_results=False):
        """Return the playoff round selections from the raw file"""

        def get_conference(series: str):
            """The conference for the teams in the series"""
            return "None" if self.playoff_round == 4 or self.year == 2021 \
                else team_conference(series[:3], self.year)

        data = self._read_data_file()
        series = self._series_from_file()
        non_series_columns = [
            col for col in data.columns
            if not bool(re.match(r"^[A-Z]{3}-[A-Z]{3}", col))
            and col != 'Individual'
        ]
        pre_pivot = (
            data
            .rename(columns=dict(list(zip(series, [f'{ser}Team' for ser in series]))))
            .drop(columns=non_series_columns)
        )
        post_pivot = (pd.wide_to_long(
                pre_pivot,
                stubnames=series,
                i='Individual',
                j='Selections',
                suffix='\\D+'
            )
            .stack()
            .unstack(-2)
            .rename_axis(index=['Individual', 'Series'])
            .pipe(
                lambda df: df.drop(index='Results')
                if not keep_results
                else df
            )
        )
        # add conference to index
        conf_index = [
            get_conference(a_series)
            for a_series in post_pivot.index.get_level_values('Series')
        ]
        post_pivot = (
            post_pivot
            .set_index(
                pd.Index(conf_index, name='Conference'),
                append=True
            )
            .reorder_levels(['Individual', 'Conference', 'Series'])
            .rename(columns={' series length:': 'Duration'})
            .replace(to_replace=math.nan, value=None)
        )
        selection_columns = ['Team', 'Duration']
        if ' Who will score more points?' in post_pivot.columns:
            post_pivot.rename(columns={' Who will score more points?': 'Player'}, inplace=True)
            selection_columns += ['Player']
        # modify duration column
        mask = (
            post_pivot
            .loc[:, 'Duration']
            .str[0]
            .isin(
                map(str, utils.series_duration_options(self.playoff_round))
            )
        )
        post_pivot.loc[~mask, 'Duration'] = [None] * len(post_pivot.loc[~mask, 'Duration'])
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                category=FutureWarning,
                message=(
                    ".*will attempt to set the values inplace instead "
                    "of always setting a new array. "
                    "To retain the old behavior, use either.*"
                ),
            )
            post_pivot.loc[mask, 'Duration'] = (
                post_pivot
                .loc[mask, 'Duration']
                .str[0]
                .astype("Int64")
            )
        return (
            post_pivot[selection_columns]
            .sort_index(
                level=["Individual", "Conference"],
                sort_remaining=False
            )
            .astype({'Duration': "Int64"})
        )

    def _load_champions_selections_from_file(self, keep_results=False):
        """Return the champions selections from the raw file"""

        def select_conference_team(row, conference):
            """Return the team in the dataframe row for a particular conference"""
            champions_headers = self._champions_headers()
            if conference != 'Stanley Cup':
                teams = row[champions_headers].values.tolist()
                return teams[0] \
                    if team_conference(teams[0], self.year) == conference \
                    else teams[1]
            return row['Who will win the Stanley Cup?']

        data = (
            self
            ._read_data_file()
            .set_index(['Individual'])
            .rename_axis(columns=['Selections'])
            .pipe(
                lambda df: df.drop(index='Results')
                if not keep_results
                else df
            )
        )

        champions_headers = ['East', 'West', 'Stanley Cup']
        for conference in champions_headers:
            data[conference] = data.apply(
                lambda row,
                conf=conference: select_conference_team(row, conf),
                axis=1
            )
        champions_headers += ['Duration']

        duration_header = 'Length of Stanley Cup Finals'
        if duration_header not in data.columns:
            data.insert(len(data.columns), 'Duration', [None]*len(data))
        else:
            data.rename(columns={duration_header: 'Duration'}, inplace=True)
            data['Duration'] = data['Duration'].str[0].astype("Int64")
        return data[champions_headers]

    def _load_playoff_round_selections_from_database(self):
        """Return the playoff round selections from the database"""
        with self.database as db:
            data = db.get_all_round_selections(self.year, self.playoff_round)
        num_individuals = len(data.index.unique())
        series_list = [subval for values in self.series.values() for subval in values]
        new_data = (
            data
            .drop(columns=['SeriesNumber'])
            .set_index('Conference', append=True)
            .set_index(
                pd.Index(series_list*num_individuals),
                append=True
            )
            .rename_axis(
                index=['Individual', 'Conference', 'Series'],
                columns=['Selections'],
            )
            .astype({'Duration': 'Int64'})
        )
        no_player_picks = all(item is None for item in data['Player'])
        if no_player_picks:
            return new_data.drop(columns=['Player'])
        return new_data

    def _load_champions_selections_from_database(self):
        """Return the Champions selections from the database"""
        with self.database as db:
            return db.get_stanley_cup_selections(self.year)

    def _series_from_file(self):
        """List the series without conference from file"""
        data = self._read_data_file()
        return [
            col for col in data.columns
            if bool(re.match(r"^[A-Z]{3}-[A-Z]{3}$", col))
            or bool(re.match(r"^[A-Z]{3}-[A-Z]{3}-[A-Z]{3}$", col))
        ]

    def _conference_series_from_file(self):
        """Turn a list of series into a dictionary of series in each conference"""

        series = self._series_from_file()

        def correct_conference(series: str, conference: str):
            """Boolean for correct conference of the teams"""
            if self.year == 2021:
                return True
            return True if self.playoff_round == 4 else \
                team_conference(series[:3], self.year) == conference \
                and team_conference(series[-3:], self.year) == conference

        return {
            conf:
            [a_series for a_series in series if correct_conference(a_series, conf)]
            for conf in self._conference_list()
        }

    def _conference_series_from_database(self):
        """Turn a list of series into a dictionary of series in each conference"""

        with self.database as db:
            series_table = db.get_all_series_in_round(self.year, self.playoff_round)
        num_series = series_table['SeriesNumber'].max()

        def series_name(conference, series_number):
            """Get the series name for a series number in a conference
            from the pandas table from the database"""
            # conference = conference if conference=="None" else f'"{conference}"'
            series_str = ','.join(
                series_table.query(
                    f'Conference in ["{conference}"] and SeriesNumber=={series_number}'
                )
                [['TeamHigherSeed', 'TeamLowerSeed']]
                .values[0]
            )
            return '-'.join(map(stn, series_str.split(',')))

        return {
            conf:
            [series_name(conf, num) for num in range(1, num_series+1)]
            for conf in self._conference_list()
        }

    def _conference_list(self):
        """List the conferences in the current playoff round"""
        if self.playoff_round == 4 or self.year == 2021:
            return ["None"]
        if self.playoff_round in utils.conference_rounds(self.year):
            return ['East', 'West']

    def _champions_headers(self):
        """List the headers for the champions picks in round 1"""
        if self.year == 2017:
            return [
                'Who will win the Stanley Cup?',
                'Who will be the Stanley Cup runner-up?'
            ]
        base_list = [
            "Who will win the Western Conference?",
            "Who will win the Eastern Conference?",
            "Who will win the Stanley Cup?"
        ]
        if self.year in [2006, 2007, 2008]:
            return base_list + ['Length of Stanley Cup Finals']
        return base_list
