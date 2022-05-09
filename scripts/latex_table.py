"""
Script for making the latex file which generate the table
of individuals selections
"""
import os
from pathlib import Path
import pandas as pd
from scripts.nhl_teams import shorten_team_name
from scripts.database import DataBaseOperations


def make_latex_file(year, playoff_round):
    '''Create the latex file from the pandas dataframe for the round'''

    db_ops = DataBaseOperations()

    # import data from database
    with db_ops as db:
        stanley_data = db.get_stanley_cup_selections(year)
        round_data = db.get_all_round_selections(year, playoff_round)
        if playoff_round in [1,2,3]:
            teams = db.get_teams_in_year_round(year, playoff_round)
        elif playoff_round == 4:
            teams = db.get_teams_in_year_round(year, playoff_round)

    # find absolute path of tables directory
    scripts_dir = Path(os.path.dirname(__file__))
    base_dir = scripts_dir.parent
    table_dir = base_dir / 'tables' / f'{year}'

    # create section of the latex file
    head_matter = create_head_matter(year)
    main_table = create_main_table(year, playoff_round, round_data, stanley_data, teams)
    end_section = create_supplementary_info(year, playoff_round, round_data, teams, base_dir)
    foot_matter = '\n\\end{document}'
    # put all section together
    all_lines = head_matter + main_table + end_section + foot_matter

    # write to document
    if not os.path.exists(table_dir):
        os.mkdir(table_dir)
    latex_filename = f"{table_dir}/round{playoff_round}.tex"
    with open(latex_filename, "w+", encoding='utf-8') as file:
        file.writelines(all_lines)

    # run tex
    latex_pdf_command = '/Library/TeX/texbin/pdflatex '\
                        f'-output-directory={table_dir} '\
                        f'{latex_filename}'
    os.system(latex_pdf_command)

def number_of_series_in_round(playoff_round):
    '''Return the number of series in the playoff round'''
    return 2**(4-playoff_round)

def number_of_series_in_round_per_conference(playoff_round):
    '''Return the number of series in a conference in the playoff round'''
    total_num_series = number_of_series_in_round(playoff_round)
    if playoff_round in [1,2,3]:
        num_series = total_num_series // 2
    elif playoff_round == 4:
        num_series = total_num_series
    else:
        raise Exception(f'The playoff round ({playoff_round}) was not recognized')
    return num_series

def number_of_columns(num_individuals):
    '''Return the number of columns in the main table'''
    return 2*num_individuals + 1


def create_head_matter(year):
    '''Create the latex imports and file title'''

    headmatter = '''
%----------------------------------------------------------------------------------------
%	Settings and packages
%----------------------------------------------------------------------------------------

\\documentclass[10pt]{article}

\\usepackage{colortbl}
\\usepackage{multirow}
\\usepackage[table]{xcolor}
\\usepackage{ctable}
\\usepackage{wrapfig}
\\usepackage[landscape,margin=0.25in,legalpaper]{geometry}

\\newcommand{\\mcn}[2]{\\multicolumn{#1}{l}{#2}}	
\\newcommand{\\mccn}[2]{\\multicolumn{#1}{c}{#2}}
\\newcommand{\\mcl}[1]{\\multicolumn{2}{l}{#1}}
\\newcommand{\\mclg}[1]{\\multicolumn{2}{l}{\\gr #1}}
\\newcommand{\\mcc}[1]{\\multicolumn{2}{c}{#1}}
\\newcommand{\\mccg}[1]{\\multicolumn{2}{c}{\\gr #1}}
\\newcommand{\\mr}[1]{\\multirow{-2}{*}{#1}}
\\definecolor{Gray}{gray}{0.90}
\\newcommand{\\gr}{\\cellcolor{Gray}}

\\newcommand{\\thickline}{\\specialrule{.1em}{.05em}{.05em}}

% column colours
\\newcolumntype{g}{>{\\columncolor{Gray}}l}
\\newcolumntype{w}{>{\\columncolor{white}}l}


%\\usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots.
%\\geometry{letterpaper}                    % ... or a4paper or a5paper or ... 
%\\geometry{landscape}                		% Activate for for rotated page geometry

%----------------------------------------------------------------------------------------
%	Create new commands
%----------------------------------------------------------------------------------------

% Commands are in LatexCommands.tex. New commands for this file only can be written here.
%\\input{/Applications/TeX/Latex_ancillary/LatexCommands.tex}


%----------------------------------------------------------------------------------------
%	Table
%----------------------------------------------------------------------------------------

\\begin{document}

\\thispagestyle{empty}
'''

    headmatter += f'{{\\bf {year} Deepwell Cup}}'
    return headmatter

def create_main_table(year, playoff_round, round_data, stanley_data, teams):
    '''Create the main table'''

    # will need to be careful about the individuals list in years when individuals enter
    # in later rounds or drop off after a few rounds
    individuals = pd.unique(round_data['Name'])
    num_individuals = len(individuals)
    num_columns = number_of_columns(num_individuals)

    table_header = '''
\\begin{table}[h!]
    \\centering
    \\begin{tabular}{l'''
    table_header += " g g w w" * (num_individuals//2)
    if num_individuals%2:
        table_header += " g g"
    table_header += "}"

    # table title and column names
    if playoff_round == 1:
        table_title = "Round 1: Division Semi-Finals"
    elif playoff_round == 2:
        table_title = "Round 2: Division Finals"
    elif playoff_round == 3:
        table_title = "Round 3: Conference Finals"
    elif playoff_round == 4:
        table_title = "Round 4: Stanley Cup Finals"
    table_title = f'''
        \\rowcolor{{black}}\\mcn{{{num_columns}}}{{\\color{{white}}\\bf {table_title}}} \\\\
        \\rowcolor{{white}}\\\\
        '''

    # table column titles (individual names)
    for ii, individual in enumerate(individuals):
        if ii%2 == 0:
            table_title += f"&  \\mccg{{{individual}}}"
        else:
            table_title += f"&  \\mcc{{{individual}}}"
    table_title += " \\\\\\thickline\n"

    # add rows of picks for each series
    if playoff_round in [1,2,3]:
        table_east = create_main_table_conference_picks(
                playoff_round, 'East', teams[0], round_data, individuals)
        table_west = create_main_table_conference_picks(
                playoff_round, 'West', teams[1], round_data, individuals)
        picks_table = table_east + table_west
    elif playoff_round == 4:
        picks_table = create_main_table_conference_picks(
                playoff_round, None, teams, round_data, individuals)

    # Conference Champion setup
    champ_section = create_main_table_stanley_picks(year, stanley_data, individuals)

    table_footer = '''
    \\end{tabular}
\\end{table}
'''

    main_table = table_header + table_title + picks_table + champ_section + table_footer
    return main_table

def create_main_table_conference_picks(playoff_round, conference, teams, round_data, individuals):
    '''Create the interior of the table of players picks
    That is, not the header or stanley cup selection portion'''

    num_columns = number_of_columns(len(individuals))
    num_series = number_of_series_in_round_per_conference(playoff_round)
    stn = shorten_team_name

    # define empty line types
    blank   = (num_columns-1)*"&"+" \\\\\\hline\n"
    blanker = (num_columns-1)*"&"+" \\\\\n"
    white = "\\rowcolor{white}\\\\\n"

    # subtitles
    conference_table = ""
    if playoff_round in [1,2,3]:
        conference_table += f"        {{\\bf {conference}}} "+(num_columns-1)*"&"+"\\\\\\hline\n"

    for nn in range(num_series):
        conference_table += "          "+teams[nn][0]  # add higher seeded team
        conference_table += (num_columns-1)*"&"+"\\\\\n"
        conference_table += "          " + teams[nn][1]  # add lower seeded team

        # deal with final round here (conference == None)
        for individual in individuals:
            if playoff_round in [1,2,3]:
                query = f'Name=="{individual}" and Conference=="{conference}"'
            elif playoff_round == 4:
                query = f'Name=="{individual}"'

            team_pick = stn(round_data.query(query)['TeamSelection'].iloc[nn])
            game_pick =     round_data.query(query)['GameSelection'].iloc[nn]
            conference_table += f" & \\mr{{{team_pick}}} & \\mr{{{game_pick}}}"
        conference_table += "\\\\\\hline\n"

        if nn == num_series-1 and conference == 'East':
            conference_table += "          "+blanker
        elif nn == num_series-1 and conference in ['West', None]:
            conference_table += "          "+white
        else:
            conference_table += "          "+blank

    return conference_table

def create_main_table_stanley_picks(year, stanley_data, individuals):
    '''Create the stanley cup picks portion of the main table of individuals picks'''

    num_columns = number_of_columns(len(individuals))
    stn = shorten_team_name

    champtitle = f'        \\rowcolor{{black}} \\mcn{{{num_columns}}}'\
                    '{\\color{white}\\bf Conference Champions} \\\\\n'
    champ_east    = "          Eastern"
    champ_west    = "          Western"
    champ_stanley = "          Stanley Cup"
    # individual's picks for the conference champions
    for ii, individual in enumerate(individuals):
        try:
            stanley_east_pick = stn(stanley_data["EastSelection"][individual])
            stanley_west_pick = stn(stanley_data["WestSelection"][individual])
            stanley_cup_pick = stn(stanley_data["StanleyCupSelection"][individual])
            stanley_game_pick = stanley_data["GameSelection"][individual]
        except KeyError:
            # the individual was not playing during the first round and had no
            # championship round selections
            stanley_east_pick = ''
            stanley_west_pick = ''
            stanley_cup_pick = ''
        if year in [2006, 2007, 2008]:
            # in 2006, 2007, and 2008 everyone picked the length of the Stanley Cup Finals
            # at the beginning of the playoffs
            if ii%2 == 0:
                champ_east    += f' & \\mclg{{{stanley_east_pick}}}'
                champ_west    += f' & \\mclg{{{stanley_west_pick}}}'
            else:
                champ_east +=    f' & \\mcl{{{stanley_east_pick}}}'
                champ_west +=    f' & \\mcl{{{stanley_west_pick}}}'
            champ_stanley += f' & {stanley_cup_pick} & {stanley_game_pick}'
        else:
            if ii%2 == 0:
                champ_east    += f' & \\mclg{{{stanley_east_pick}}}'
                champ_west    += f' & \\mclg{{{stanley_west_pick}}}'
                champ_stanley += f' & \\mclg{{{stanley_cup_pick}}}'
            else:
                champ_east +=    f' & \\mcl{{{stanley_east_pick}}}'
                champ_west +=    f' & \\mcl{{{stanley_west_pick}}}'
                champ_stanley += f' & \\mcl{{{stanley_cup_pick}}}'
    champ_east += "\\\\\n"
    champ_west += "\\\\\n"

    champ_section = champtitle + champ_east + champ_west + champ_stanley
    return champ_section

def create_supplementary_info(year, playoff_round, round_data, teams, base_dir):
    '''Create the bottom portion of the document
    That is, the points system, and counts of picks per team'''

    stn = shorten_team_name
    num_series = number_of_series_in_round(playoff_round)

    end_section_start = '\n\\begin{table}[!htb]'

    # tables describing the scoring system
    points_tables = '''
\\begin{minipage}[t]{.27\\linewidth}
{\\bf Points}\\\\
\\begin{tabular}{l l}
    Correct team:	& $10$\\\\
    Correct series length (regardless of series winner):	& $7$\\\\
    Correct team in a seven game series    & $2$\\\\
    Stanley Cup champion:	& 25\\\\
    Stanley Cup runner-up:	& 15\\\\
\\end{tabular}
\\hspace{0.5cm}'''
# %
# \\begin{minipage}[t]{0.12\\linewidth}
# \\qquad Correct team\\\\
# \\begin{tabular}{c l | c c c c }
#     \\mccn{2}{} & \\mccn{4}{Predicted}\\\\
#     & & 4 & 5 & 6 & 7\\\\\\cline{2-6}
#     \\parbox[t]{2mm}{\\multirow{4}{*}{\\rotatebox[origin=c]{90}{Actual}}}& 4 & 15 & 13 & 11 & 9\\\\
#     & 5 & 13 & 15 & 13 & 11\\\\
#     & 6 & 11 & 13 & 15 & 13\\\\
#     & 7 &  9 & 11 & 13 & 15
# \\end{tabular}
# \\end{minipage}
# %
# \\begin{minipage}[t]{0.12\\linewidth}
# \\qquad Incorrect team\\\\
# \\begin{tabular}{c l | c c c c }
#     \\mccn{2}{} & \\mccn{4}{Predicted}\\\\
#     & & 4 & 5 & 6 & 7\\\\\\cline{2-6}
#     \\parbox[t]{2mm}{\\multirow{4}{*}{\\rotatebox[origin=c]{90}{Actual}}}&4 & 0 & 1 & 2 & 3\\\\
#     &5 & 1 & 2 & 3 & 4\\\\
#     &6 & 2 & 3 & 4 & 5\\\\
#     &7 & 3 & 4 & 5 & 6
# \\end{tabular}
# \\end{minipage}'''
    if playoff_round in [2,3,4]:
        points_tables += f'''
\\begin{{wrapfigure}}{{r}}{{0.01\\textwidth}}
    \\vspace{{-3cm}}
	\\includegraphics[width=5in]{{{base_dir}/figures/{year}/Points-{year}-Round{playoff_round-1}.pdf}}
\\end{{wrapfigure}}
\\end{{minipage}}
\\end{{table}}
'''
    else:
        points_tables += '''
\\end{minipage}
\\end{table}
'''

    # tables listing the number of picks per team
    summed_picks_start = f'''
\\begin{{minipage}}[t]{{.45\\linewidth}}
{{\\bf Number of picks per team:}}\\\\
\\begin{{tabular}}{{lc {(num_series-1)*"| lc "}}}
'''

    higher_seed_line = "    "
    lower_seed_line  = "    "
    picks_per_team = round_data['TeamSelection'].value_counts()
    if playoff_round in [1,2,3]:
        all_teams = teams[0]+ teams[1]
    elif playoff_round == 4:
        all_teams = teams
    for series in all_teams:
        higher_seed = series[0]
        lower_seed  = series[1]
        try:
            higher_counts = picks_per_team[higher_seed]
        except KeyError:
            higher_counts = 0
        try:
            lower_counts  = picks_per_team[lower_seed]
        except KeyError:
            lower_counts = 0
        higher_seed_line += f'{stn(higher_seed)} & {higher_counts} & '
        lower_seed_line  += f'{stn(lower_seed) } & {lower_counts } & '

    higher_seed_line = higher_seed_line[:-2]+"\\\\\n"
    lower_seed_line  =  lower_seed_line[:-2]+"\\\\"

    summed_picks_finish = '''
\\end{tabular}
\\end{minipage}
'''
    summed_picks_table = summed_picks_start + higher_seed_line + \
                            lower_seed_line + summed_picks_finish

    end_section = end_section_start + points_tables + summed_picks_table
    return end_section
