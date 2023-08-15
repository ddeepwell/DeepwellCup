"""Class for making LaTex table files"""
import os
from numpy import array
from pandas import isna
from sympy import latex, symbols
from sympy.utilities.lambdify import lambdify
from jinja2 import Environment, FileSystemLoader
from deepwellcup.processing import dirs, utils
from deepwellcup.processing.selections import Selections
from deepwellcup.processing.scores import IndividualScoring
from deepwellcup.processing.nhl_teams import (
    shorten_team_name as stn,
    lengthen_team_name as ltn,
)
from .utils import DataStores


class Latex():
    """Class making LaTex table files"""

    def __init__(
        self,
        year,
        playoff_round,
        datastores: DataStores = DataStores(None, None),
    ):
        self._year = year
        self._playoff_round = playoff_round
        self._round_selections = Selections(
            year=year,
            playoff_round=playoff_round,
            datastores=datastores,
        )
        if playoff_round != 'Q':
            self._champions_selections = Selections(
                year=year,
                playoff_round='Champions',
                datastores=datastores,
            )
        else:
            self._champions_selections = None
        self._system = IndividualScoring(self.year).scoring_system()

    @property
    def year(self):
        """The year"""
        return self._year

    @property
    def playoff_round(self):
        """The playoff round"""
        return self._playoff_round

    @property
    def individuals(self):
        """The individuals in the playoff round"""
        return sorted(
            self
            ._selections
            .index
            .get_level_values('Individual')
            .unique()
        )

    @property
    def _long_form(self):
        """Whether to use long forms of team names or not"""
        if self.year > 2018:
            return False
        return True

    def _make_directory_if_missing(self, directory):
        """Create a directory is it doesn't exist"""
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _import_template(self, template):
        loader = FileSystemLoader(dirs.templates())
        environment = Environment(loader=loader)
        return environment.get_template(template)

    def _write_file(self, filename, contents):
        """Write to a file"""
        with open(filename, "w+", encoding='utf-8') as file:
            file.writelines(contents)

    def _build_pdftex(self, source_file, quiet=True):
        """Build the PDF from the Latex file"""
        cwd = os.getcwd()
        os.chdir(dirs.year_tables(self.year))
        build_command = f'/Library/TeX/texbin/pdflatex -halt-on-error {source_file}'
        if quiet:
            build_command += " > /dev/null"
        os.system(build_command)
        os.chdir(cwd)

    # class PlayoffRoundTable():
    #     """Subclass for making the table of selections in a playoff round"""

    #     def __init__(self):
    #         self.year = Tables.year
    #         self.playoff_round = Tables.playoff_round
    #         print(self.playoff_round)
    #         # self.selections = Tables._selections

    @property
    def latex_file(self):
        """Return the name of the LaTex file"""
        return dirs.year_tables(self.year) / f"round{self.playoff_round}.tex"

    def build_pdf(self, quiet=True):
        """Build the PDF for the selections in a playoff round"""
        self._build_pdftex(self.latex_file, quiet)

    def make_table(self):
        """Write contents of the LaTex file for a playoff round to disk"""
        self._make_directory_if_missing(dirs.year_tables(self.year))
        contents = self._make_table_contents()
        self._write_file(self.latex_file, contents)

    def _make_table_contents(self):
        """Collect the contents of the LaTex file for a playoff round"""

        if self.playoff_round == 'Q':
            previous_round = ''
        else:
            previous_round = self.playoff_round - 1
        ranking_image_path = "../../figures/"\
            f"{self.year}/Points-{self.year}-Round{previous_round}.pdf"

        template = self._import_template("round_selections.j2")
        return template.render(
            year=self.year,
            playoff_round=self.playoff_round,
            main_table=self._make_main_table(),
            scoring_table=self._make_scoring_table(),
            counts_table=self._make_counts_table(),
            correct_points=self._correct_points_table(),
            incorrect_points=self._incorrect_points_table(),
            ranking_image_path=ranking_image_path
        )

    @property
    def _number_of_columns(self):
        '''Return the number of columns in the main table'''
        return 2 * len(self.individuals) + 1

    @property
    def _selections(self):
        """Return the selections"""
        return self._round_selections.selections

    @property
    def _series(self):
        """Return the dictionary of series in each conference"""
        return self._round_selections.series

    @property
    def _players(self):
        """Return the dictionary of series in each conference"""
        return self._round_selections.players

    @property
    def _number_of_series_in_round(self):
        '''Return the number of series in the playoff round'''
        return sum(len(elem) for elem in self._series.values())

    @property
    def _number_of_series_in_round_per_conference(self):
        '''Return the number of series in a conference in the playoff round'''
        return self._number_of_series_in_round // len(self._round_selections.series)

    def _make_main_table(self):
        """Create the main table"""

        num_individuals = len(self.individuals)
        column_format = 'l' + " g g w w" * (num_individuals // 2) \
                        + (" g g" if num_individuals % 2 else "")

        # table title and column names
        if self.playoff_round == 'Q':
            table_title = "Qualification Round"
        elif self.playoff_round == 1:
            table_title = "Round 1: Division Semi-Finals"
        elif self.playoff_round == 2:
            table_title = "Round 2: Division Finals"
        elif self.playoff_round == 3:
            table_title = "Round 3: Conference Finals"
        elif self.playoff_round == 4:
            table_title = "Round 4: Stanley Cup Finals"

        if self._round_selections.preferences_selected:
            round_table = self._preferences_rows()
        else:
            round_table = self.blank if 'None' in self._series.keys() else ""

        for conference in self._series:
            round_table += self._selections_table_conference(conference)

        if self._round_selections.overtime_selected:
            round_table += self._overtime_rows()

        template = self._import_template("main_selections_table.j2")
        return template.render(
            column_format=column_format,
            num_columns=self._number_of_columns,
            table_title=table_title,
            column_header=self._names_row(),
            round_table=round_table,
            champions_table=self._champions_table()
        )

    def _names_row(self):
        """Create the row with individuals names or monikers"""
        column_header = ''
        for index, individual in enumerate(self.individuals):
            name = (
                self._round_selections.monikers[individual]
                if (
                    self._round_selections.monikers
                    and self._round_selections.monikers[individual] != ''
                )
                else individual
            )
            if index % 2 == 0:
                column_header += f"& \\mccg{{{name}}} "
            else:
                column_header += f"& \\mcc{{{name}}} "
        column_header += r" \\\thickline"
        return column_header

    def _preferences_rows(self):
        """Create rows of preferences"""
        favourite_line = 'Favourite Team'
        cheering_line = 'Cheering Team'
        for index, individual in enumerate(self.individuals):
            preferences = self._round_selections.preferences.loc[individual]
            if index % 2 == 0:
                favourite_line += f" & \\mclg{{{stn(preferences['Favourite Team'])}}}"
                cheering_line += f" & \\mclg{{{stn(preferences['Cheering Team'])}}}"
            else:
                favourite_line += f" & \\mcl{{{stn(preferences['Favourite Team'])}}}"
                cheering_line += f" & \\mcl{{{stn(preferences['Cheering Team'])}}}"
        final_line = "        " + self.blanker if self.playoff_round != 4 \
            else "        " + self.blank
        return "        " + self.blank \
            + f"        {favourite_line} \\\\\n " \
            + f"        {cheering_line} \\\\\\hline\n" \
            + final_line

    def _create_row(self, series):
        """Create a single row of the main column"""
        return self._row_team_selection(series) \
            + self._row_player_selection(series)

    def _row_team_selection(self, series):
        """Create the team selection component for a row"""
        def a_selection(individual):
            series_selections = self._selections.loc[:, :, series]
            team = stn(series_selections['Team'][individual][0])
            duration = series_selections['Duration'][individual][0]
            duration = duration if not isna(duration) else ""
            return f"& \\mr{{{team}}} & \\mr{{{duration}}}"

        if self._long_form:
            modify_team = ltn
        else:
            def modify_team(arg):
                return arg
            # modify_team = lambda arg: arg

        higher_seed = modify_team(series.split('-')[0])
        lower_seed = modify_team(series.split('-')[1])
        first_row = f"          {higher_seed}{'&'*(self._number_of_columns-1)}\\\\\n"
        second_row = f"          {lower_seed} " \
            + ' '.join([a_selection(individual) for individual in self.individuals])
        if self._round_selections.players_selected:
            second_row += r"\\" + "\n"
        else:
            second_row += r"\\\hline" + "\n"
        return first_row + second_row

    def _row_player_selection(self, series_name):
        """Create the player selection component for a row"""
        if not self._round_selections.players_selected:
            return ""

        def a_selection(index, individual):
            selections = self._selections
            player = shorten_player_name(selections['Player'][individual, :, series_name][0])
            if index % 2:
                return f"& \\mcl{{{player}}} "
            return f"& \\mclg{{{player}}} "

        return "          Player" \
            + ' '.join(
                [
                    a_selection(index, individual)
                    for index, individual in enumerate(self.individuals)
                ]
            ) \
            + r"\\\hline" + "\n"

    def _selections_table_conference(self, conference):
        '''Create the interior of the table of individuals selections
        That is, not the header or stanley cup selection portion'''

        num_columns = self._number_of_columns
        num_series = self._number_of_series_in_round_per_conference

        # subtitles
        conference_table = ""
        if conference != 'None':
            conference_table += f"        {{\\bf {conference}}} " \
                + (num_columns - 1) * "&" + "\\\\\\hline\n"
        for index, series in enumerate(self._series[conference]):
            conference_table += self._create_row(series)

            if index == num_series - 1 and conference == 'East':
                conference_table += "          " + self.blanker
            elif index == num_series - 1 and conference in ['West', "None"]:
                conference_table = conference_table[:-1]
            else:
                conference_table += "          " + self.blank

        return conference_table

    def _overtime_rows(self):
        """Row for the overtime selections"""
        row = f"{self.blanker}          Overtime"
        for index, individual in enumerate(self.individuals):
            if index % 2 == 0:
                row += f' & \\mclg{{{self._round_selections.selections_overtime[individual]}}}'
            else:
                row += f' & \\mcl{{{self._round_selections.selections_overtime[individual]}}}'
        row += "\\\\\n"
        return row

    def _champions_table(self):
        """Create the Champions table"""
        if self.playoff_round == 'Q':
            return ""
        east = self._champions_row('East')
        west = self._champions_row('West')
        stanley = self._champions_row('Stanley Cup')
        return east + west + stanley

    def _champions_row(self, category):
        """Return a row in the champions table"""

        selections = self._champions_selections.selections

        if category in ['East', 'West']:
            row_name = f'{category}ern'
        else:
            row_name = 'Stanley Cup'

        row = f"          {row_name}"
        for index, individual in enumerate(self.individuals):
            if individual in selections.index:
                selection = stn(selections.loc[individual][category])
                duration = selections.loc[individual]['Duration']
            else:
                selection = ''
                duration = None

            if duration is not None and category == "Stanley Cup":
                row += f' & {selection} & {duration}'
            else:
                if index % 2 == 0:
                    row += f' & \\mclg{{{selection}}}'
                else:
                    row += f' & \\mcl{{{selection}}}'

        if category != 'Stanley Cup':
            row += '\\\\\n'

        return row

    def _make_scoring_table(self):
        """Create the scoring table"""

        template = self._import_template("plain_table.j2")
        return template.render(
            column_format='l l',
            scoring_table=self._scoring_table_contents()
        )

    def _scoring_table_contents(self):
        """Create the contents of the scoring table"""

        system = self._system

        # Series winner and series length points descriptor
        if "correct_team_rounds_123" in system:
            descriptor = (
                "        Correct team (rounds 1,2,3):	"
                f"& ${system['correct_team_rounds_123']}$\\\\\n"
                "        Correct series length (rounds 1,2,3 - regardless of series winner):	"
                f"& ${system['correct_length_rounds_123']}$\\\\\n"
                f"        Correct team (round 4):	& ${system['correct_team_rounds_4']}$\\\\\n"
                "        Correct series length (round 4 - regardless of series winner):	"
                f"& ${system['correct_length_rounds_4']}$\\\\"
            )
        elif "correct_team" in system:
            descriptor = \
                f'''        Correct team:	& ${system['correct_team']}$\\\\
        Correct series length (regardless of series winner):	& ${system['correct_length']}$\\\\'''
        elif "f_correct" in system:
            if self.playoff_round == 'Q':
                correct_handle = 'f_correct_round_Q'
                incorrect_handle = 'f_incorrect_round_Q'
            else:
                correct_handle = 'f_correct'
                incorrect_handle = 'f_incorrect'
            C, P = symbols("C P")
            correct = latex(eval(system[correct_handle]))
            incorrect = latex(eval(system[incorrect_handle]))
            descriptor = \
                f'''        Let $C$ be the correct number of games\\\\
        Let $P$ be the predicted number of games\\\\
        If correct team chosen:	   & ${correct}$\\\\
        if incorrect team chosen:  & ${incorrect}$\\\\'''

        # Stanley Cup and other points descriptor
        if "correct_7game_series" in system:
            descriptor += f'''
        Correct team in a seven game series    & ${system['correct_7game_series']}$\\\\
        Stanley Cup champion:	& {system['stanley_cup_winner']}\\\\
        Stanley Cup runner-up:	& {system['stanley_cup_runnerup']}\\\\'''
        elif "stanley_cup_finalist" in system:
            descriptor += f'''
        Stanley Cup champion:	& {system['stanley_cup_winner']}\\\\
        Stanley Cup finalist:	& {system['stanley_cup_finalist']}\\\\'''
        elif "stanley_cup_runnerup" in system:
            descriptor += f'''
        Stanley Cup champion:	& {system['stanley_cup_winner']}\\\\
        Stanley Cup runner-up:	& {system['stanley_cup_runnerup']}\\\\'''

        # Other points
        if "Player" in system:
            descriptor += f'''
        Player:                 & {system['Player']}\\\\'''
        if "Overtime" in system:
            descriptor += f'''
        Overtime:               & {system['Overtime']}\\\\
        Overtime (1 game off):  & {system['Overtime (1 game off)']}\\\\'''

        return descriptor

    def _make_counts_table(self):
        """Create the counts table"""

        num_series = self._number_of_series_in_round

        template = self._import_template("plain_table.j2")
        return template.render(
            column_format="lc " + (num_series - 1) * "| lc ",
            scoring_table=self._counts_table_contents()
        )

    def _counts_table_contents(self):
        """Create the contents for the counts table"""
        return self._counts_table_teams() \
            + self._counts_table_players() \
            + self._counts_table_overtime()

    def _counts_table_teams(self):
        """Create the team counts for the counts table"""

        picks_per_team = self._selections['Team'].value_counts()
        series = [
            tuple(series.split('-'))
            for conference_series in self._series.values()
            for series in conference_series
        ]

        def team_counts_string(team):
            counts = (
                picks_per_team[ltn(team)]
                if ltn(team) in picks_per_team
                else 0
            )
            return f'{team} & {counts} & '

        def team_counts_line(teams):
            line = "        "
            for team in teams:
                line += team_counts_string(team)
            return line[:-2] + r"\\"

        count_strings = [team_counts_line(teams) for teams in list(zip(*series))]
        count_strings[0] = count_strings[0] + '\n'
        if self.year == 2021 and self.playoff_round == 2:
            count_strings[1] = count_strings[1] + '\n'
            third_team = series[1][2]
            count = picks_per_team[ltn(third_team)]
            count_strings += [f"        & & {third_team} & {count} & & & &" + r'\\']

        return ''.join(count_strings)

    def _counts_table_players(self):
        """Create the players counts for the counts table"""
        if not self._round_selections.players_selected:
            return ""

        picks_per_player = self._selections['Player'].value_counts()
        players = [
            tuple(series_players)
            for conference_players in self._players.values()
            for series_players in conference_players
        ]

        higher_seed_line = "        "
        lower_seed_line = "        "
        for higher_seed, lower_seed in players:
            higher_counts = picks_per_player[higher_seed] \
                if higher_seed in picks_per_player else 0
            lower_counts = picks_per_player[lower_seed] \
                if lower_seed in picks_per_player else 0
            higher_seed_line += f'{higher_seed.split(" ")[1]} & {higher_counts} & '
            lower_seed_line += f'{lower_seed.split(" ")[1]} & {lower_counts } & '

        higher_seed_line = higher_seed_line[:-2] + "\\\\\n"
        lower_seed_line = lower_seed_line[:-2] + "\\\\"

        return "\n" + higher_seed_line + lower_seed_line

    def _counts_table_overtime(self):
        """Create the overtime counts for the counts table"""
        if not self._round_selections.overtime_selected:
            return ""

        picks_per_length = self._round_selections.selections_overtime.value_counts()
        lengths = ['0', '1', '2', '3', "More than 3"]
        length_line = "\n"
        for length in lengths:
            value = picks_per_length[length] if length in picks_per_length.index else 0
            vspace = r"\rule{0pt}{3.5ex}" if length == '0' else ""
            length_line += f"        {vspace}{length} & {value}" + "\\\\\n"
        return length_line[:-3]

    def _correct_points_table(self):
        """Create the points table for the correctly selected team"""
        system = self._system
        if 'f_correct' not in system:
            return None
        if self.playoff_round == 'Q':
            handle = 'f_correct_round_Q'
        else:
            handle = 'f_correct'
        C, P = symbols("C P")
        f_correct = lambdify((C, P), system[handle], "numpy")
        return self._points_table(f_correct)

    def _incorrect_points_table(self):
        """Create the points table for the incorrectly selected team"""
        system = self._system
        if 'f_incorrect' not in system:
            return None
        if self.playoff_round == 'Q':
            handle = 'f_incorrect_round_Q'
        else:
            handle = 'f_incorrect'
        C, P = symbols("C P")
        f_incorrect = lambdify((C, P), system[handle], "numpy")
        return self._points_table(f_incorrect)

    def _points_table(self, func):
        """Return the table of points per predicted and correct series duration"""
        if self.playoff_round == 'Q':
            return (
                r"""        \mccn{2}{} & \mccn{3}{Predicted}\\
        & & 3 & 4 & 5\\\cline{2-4}""" + '\n'
                + r"        \parbox[t]{2mm}{\multirow{3}{*}{\rotatebox[origin=c]{90}{Correct}}}"
                + f" & 3 & {self._make_points_string(func, 3)}" + r"\\" + '\n'
                + f"        & 4 & {self._make_points_string(func, 4)}" + r"\\" + '\n'
                + f"        & 5 & {self._make_points_string(func, 5)}"
            )
        return (
            r"""        \mccn{2}{} & \mccn{4}{Predicted}\\
        & & 4 & 5 & 6 & 7\\\cline{2-6}""" + '\n'
            + r"        \parbox[t]{2mm}{\multirow{4}{*}{\rotatebox[origin=c]{90}{Correct}}}"
            + f" & 4 & {self._make_points_string(func, 4)}" + r"\\" + '\n'
            + f"        & 5 & {self._make_points_string(func, 5)}" + r"\\" + '\n'
            + f"        & 6 & {self._make_points_string(func, 6)}" + r"\\" + '\n'
            + f"        & 7 & {self._make_points_string(func, 7)}"
        )

    def _make_points_string(self, func, correct_games):
        """Create the string for the points for a specific series duration"""
        return " & ".join(
            func(correct_games, array(utils.series_duration_options(self.playoff_round)))
            .astype(str)
            .tolist()
        )

    @property
    def blank(self):
        """Return an empty line which matches the column colouring
        and has a thin horizontal black line below the line"""
        return (self._number_of_columns - 1) * "&" + " \\\\\\hline\n"

    @property
    def blanker(self):
        """Return an empty line which matches the column colouring"""
        return (self._number_of_columns - 1) * "&" + " \\\\\n"


def shorten_player_name(name):
    """Shorten a player name"""
    last_name = name.split(' ')[1]
    num_letters = min(len(last_name), 7)
    return last_name[:num_letters]
