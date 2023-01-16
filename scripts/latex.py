"""Class for making LaTex table files"""
import os
from numpy import array
from pandas import isna
from sympy import latex, symbols
from sympy.utilities.lambdify import lambdify
from jinja2 import Environment, FileSystemLoader
from scripts.selections import Selections
from scripts.directories import project_directory
from scripts.scores import IndividualScoring
from scripts.nhl_teams import (
    shorten_team_name as stn,
    lengthen_team_name as ltn
)

class Latex():
    """Class making LaTex table files"""

    def __init__(self, year, playoff_round, selections_directory=None, **kwargs):
        self._year = year
        self._playoff_round = playoff_round
        self._round_selections = Selections(
            year=year,
            playoff_round=playoff_round,
            selections_directory=selections_directory,
            **kwargs)
        self._champions_selections = Selections(
            year=year,
            playoff_round='Champions',
            selections_directory=selections_directory,
            **kwargs)
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
            self._round_selections.selections.index.get_level_values('Individual').unique()
        )

    @property
    def _long_form(self):
        """Whether to use long forms of team names or not"""
        if self.year == 2019:
            return False
        return True

    def _make_directory_if_missing(self, directory):
        """Create a directory is it doesn't exist"""
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _year_tables_directory(self):
        return project_directory()/f'tables/{self.year}'

    def _import_template(self, template):
        loader = FileSystemLoader(project_directory()/'scripts/templates/')
        environment = Environment(loader=loader)
        return environment.get_template(template)

    def _write_file(self, filename, contents):
        """Write to a file"""
        with open(filename, "w+", encoding='utf-8') as file:
            file.writelines(contents)

    def _build_pdftex(self, source_file, quiet=True):
        """Build the PDF from the Latex file"""
        cwd = os.getcwd()
        os.chdir(self._year_tables_directory())
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
    #         # self.selections = Tables._round_selections.selections

    @property
    def latex_file(self):
        """Return the name of the LaTex file"""
        return self._year_tables_directory() / f"round{self.playoff_round}.tex"

    def build_pdf(self, quiet=True):
        """Build the PDF for the selections in a playoff round"""
        self._build_pdftex(self.latex_file, quiet)

    def make_table(self):
        """Write contents of the LaTex file for a playoff round to disk"""

        self._make_directory_if_missing(self._year_tables_directory())
        contents = self._make_table_contents()
        self._write_file(self.latex_file, contents)

    def _make_table_contents(self):
        """Collect the contents of the LaTex file for a playoff round"""

        ranking_image_path = "../../figures/"\
            f"{self.year}/Points-{self.year}-Round{self.playoff_round-1}.pdf"

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
        return 2*len(self.individuals) + 1

    @property
    def _number_of_series_in_round(self):
        '''Return the number of series in the playoff round'''
        return sum(len(elem) for elem in self._round_selections.series.values())

    @property
    def _number_of_series_in_round_per_conference(self):
        '''Return the number of series in a conference in the playoff round'''
        if self.playoff_round in [1,2,3]:
            return self._number_of_series_in_round//2
        return self._number_of_series_in_round

    def _make_main_table(self):
        """Create the main table"""

        num_individuals = len(self.individuals)
        column_format = 'l' + " g g w w"*(num_individuals//2) \
                        + (" g g" if num_individuals%2 else "")

        # table title and column names
        if self.playoff_round == 1:
            table_title = "Round 1: Division Semi-Finals"
        elif self.playoff_round == 2:
            table_title = "Round 2: Division Finals"
        elif self.playoff_round == 3:
            table_title = "Round 3: Conference Finals"
        elif self.playoff_round == 4:
            table_title = "Round 4: Stanley Cup Finals"

        # column headers
        column_header = ''
        for index, individual in enumerate(self.individuals):
            if index % 2 == 0:
                column_header += f"&  \\mccg{{{individual}}}"
            else:
                column_header += f"&  \\mcc{{{individual}}}"
        column_header += r" \\\thickline"

        round_table = ''
        for conference in self._round_selections.series:
            round_table += self._selections_table_conference(conference)

        template = self._import_template("main_selections_table.j2")
        return template.render(
            column_format=column_format,
            num_columns=self._number_of_columns,
            table_title=table_title,
            column_header=column_header,
            round_table=round_table,
            champions_table=self._champions_table()
        )

    def _create_row(self, series):
        """Create a single row of the main column"""

        def a_selection(individual):
            series_selections = self._round_selections.selections.loc[:,:,series]
            team = stn(series_selections.loc[individual]['Team'][0])
            duration = series_selections.loc[individual]['Duration'][0]
            duration = duration if not isna(duration) else ""
            return f"& \\mr{{{team}}} & \\mr{{{duration}}}"

        if self._long_form:
            modify_team = ltn
        else:
            modify_team = lambda arg: arg

        higher_seed = modify_team(series.split('-')[0])
        lower_seed  = modify_team(series.split('-')[1])
        first_part = f"          {higher_seed}{'&'*(self._number_of_columns-1)}\\\\\n"
        second_part = f"          {lower_seed} " \
            + ' '.join([a_selection(individual) for individual in self.individuals]) \
            + r"\\\hline"+"\n"
        return first_part + second_part

    def _selections_table_conference(self, conference):
        '''Create the interior of the table of individuals selections
        That is, not the header or stanley cup selection portion'''

        num_columns = self._number_of_columns
        num_series = self._number_of_series_in_round_per_conference

        # define empty line types
        blank   = (num_columns-1)*"&"+" \\\\\\hline\n"
        blanker = (num_columns-1)*"&"+" \\\\\n"

        # subtitles
        conference_table = ""
        if self.playoff_round in [1,2,3]:
            conference_table += f"        {{\\bf {conference}}} "+(num_columns-1)*"&"+"\\\\\\hline\n"
        for index, series in enumerate(self._round_selections.series[conference]):
            conference_table += self._create_row(series)

            if index == num_series-1 and conference == 'East':
                conference_table += "          "+blanker
            elif index == num_series-1 and conference in ['West', "None"]:
                conference_table = conference_table[:-1]
            else:
                conference_table += "          "+blank

        return conference_table

    def _champions_table(self):
        """Create the Champions table"""
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
            descriptor = \
f'''        Correct team (rounds 1,2,3):	& ${system['correct_team_rounds_123']}$\\\\
        Correct series length (rounds 1,2,3 - regardless of series winner):	& ${system['correct_length_rounds_123']}$\\\\
        Correct team (round 4):	& ${system['correct_team_rounds_4']}$\\\\
        Correct series length (round 4 - regardless of series winner):	& ${system['correct_length_rounds_4']}$\\\\'''
        elif "correct_team" in system:
            descriptor = \
f'''        Correct team:	& ${system['correct_team']}$\\\\
        Correct series length (regardless of series winner):	& ${system['correct_length']}$\\\\'''
        elif "f_correct" in system:
            C, P = symbols("C P")
            correct = latex(eval(system['f_correct']))
            incorrect = latex(eval(system['f_incorrect']))
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
            column_format="lc "+(num_series-1)*"| lc ",
            scoring_table=self._counts_table_contents()
        )

    def _counts_table_contents(self):
        """Create the contents for the counts table"""

        picks_per_team = self._round_selections.selections['Team'].value_counts()
        series = [tuple(series.split('-'))
                    for conference_series in self._round_selections.series.values()
                    for series in conference_series]

        higher_seed_line = "        "
        lower_seed_line  = "        "
        for higher_seed, lower_seed in series:
            higher_counts = picks_per_team[ltn(higher_seed)] \
                if ltn(higher_seed) in picks_per_team else 0
            lower_counts = picks_per_team[ltn(lower_seed)] \
                if ltn(lower_seed) in picks_per_team else 0
            higher_seed_line += f'{higher_seed} & {higher_counts} & '
            lower_seed_line  += f'{lower_seed} & {lower_counts } & '

        higher_seed_line = higher_seed_line[:-2]+"\\\\\n"
        lower_seed_line  =  lower_seed_line[:-2]+"\\\\"

        return higher_seed_line + lower_seed_line

    def _correct_points_table(self):
        """Create the points table for the correctly selected team"""
        system = self._system
        if 'f_correct' not in system:
            return None
        C, P = symbols("C P")
        f_correct = lambdify((C, P), system['f_correct'], "numpy")
        return self._points_table(f_correct)

    def _incorrect_points_table(self):
        """Create the points table for the incorrectly selected team"""
        system = self._system
        if 'f_incorrect' not in system:
            return None
        C, P = symbols("C P")
        f_incorrect = lambdify((C, P), system['f_incorrect'], "numpy")
        return self._points_table(f_incorrect)

    def _points_table(self, func):
        """Return the table of points per predicted and correct series duration"""
        return r"""        \mccn{2}{} & \mccn{4}{Predicted}\\
        & & 4 & 5 & 6 & 7\\\cline{2-6}""" + '\n' \
            + r"        \parbox[t]{2mm}{\multirow{4}{*}{\rotatebox[origin=c]{90}{Correct}}}" \
            + f" & 4 & {self._make_points_string(func, 4)}" + r"\\" + '\n' \
            + f"        & 5 & {self._make_points_string(func, 5)}" + r"\\" + '\n' \
            + f"        & 6 & {self._make_points_string(func, 6)}" + r"\\" + '\n' \
            + f"        & 7 & {self._make_points_string(func, 7)}"

    def _make_points_string(self, func, correct_games):
        """Create the string for the points for a specific series duration"""
        return " & ".join(func(correct_games, array([4,5,6,7])).astype(str).tolist())
