'''
Functions for creating plots
'''
import os
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scripts.scoring import year_points_table

# set font to look like Latex
font = {'family' : 'serif',
        'size'   : 12}
mpl.rc('font', **font)

def year_chart(year, max_round='Champions', save=False):
    '''Create a bar chart of the points standings in a year
    '''

    points_unsorted_df = year_points_table(year)
    round_names = points_unsorted_df.index[:-1].tolist()

    # parse which rounds to plot
    # In some years, after the third round you some individuals
    # may have points from their champions selection and this should be reflected in the plot
    # will add this later
    if max_round in [1,2,3,4]:
        max_round_name = f'Round {max_round}'
    else:
        max_round_name = max_round
    max_round_index = round_names.index(max_round_name)
    rounds_to_plot = round_names[:max_round_index+1]
    max_points = points_unsorted_df.loc[rounds_to_plot].sum().max()

    # sort individuals by total score
    player_rankings = points_unsorted_df.loc[rounds_to_plot].sum().sort_values(ascending=True).index
    points_df = points_unsorted_df.reindex(player_rankings, axis='columns')

    # gather extra data
    individuals = points_df.columns
    num_individuals = len(individuals)

    # set plot colours
    round_colors = ['#95c4e8','#a3e6be','#fbee9d','#fbbf9d','#e29dfb']
    colors = dict(zip(round_names, round_colors))

    # set-up figure
    fig = plt.figure(figsize=(8, 0.5*num_individuals))
    axis = fig.add_subplot(111)

    for individual_i, individual in enumerate(individuals):
        left = 0
        axis_list = []
        for playoff_round in rounds_to_plot:
            round_points = points_df[individual][playoff_round]
            if not np.isnan(round_points):
                axis_list.append(
                    axis.barh(individual_i, round_points,
                                left = left,
                                align = 'center',
                                edgecolor = 'black',
                                color = colors[playoff_round],
                                label = playoff_round
                    )
                )
                # add text
                patch = axis_list[-1][0]
                left_patch_position, bottom_patch_position = patch.get_xy()
                x_round = 0.5*patch.get_width() + left_patch_position
                y_individual = 0.5*patch.get_height() + bottom_patch_position
                # if round_points != 0:
                axis.text(x_round, y_individual, f'{round_points}', ha='center', va='center')
                left += round_points
            if playoff_round == rounds_to_plot[-1]:
                # add total sum of points outside bar graph
                x_total = left + max_points/25
                total_points = points_df[individual].loc[rounds_to_plot].sum()
                axis.text(x_total, y_individual, f'{total_points}', ha='center',va='center')

    # set axis and add labels
    y_pos = np.arange(num_individuals)
    axis.set_yticks(y_pos)
    axis.set_yticklabels(individuals)
    axis.set_xlim(0, max_points*1.02)
    fig_title = f'Points - {year}'
    if max_round_name != 'Champions':
        fig_title = f'{fig_title} - {max_round_name}'
    # add functionality for incomplete years
    # add Round to title even without specifying max_round
    plt.title(fig_title)

    # remove axis lines
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.yaxis.set_ticks_position('none')
    axis.xaxis.set_ticks_position('none')
    axis.get_xaxis().set_ticks([])

    add_legend(axis_list)
    if save:
        # save figure for year
        file_name = fig_title.replace(' ','')
        save_figure(file_name, year)


def add_legend(axis_list):
    '''Add a legend'''

    # remove unused elements of a_bar
    a_bar2 = list(filter(lambda a: a != 0, axis_list))

    # Put a legend to the right of the current axis
    plt.legend(handles=a_bar2, loc='center left', bbox_to_anchor=(1.05,0.5))

def save_figure(file_name, year):
    '''Save to disk'''
    scripts_dir = Path(os.path.dirname(__file__))
    base_dir = scripts_dir.parent
    figure_dir = base_dir / 'figures' / f'{year}'
    if not os.path.exists(figure_dir):
        os.mkdir(figure_dir)
    plt.savefig(f'{figure_dir}/{file_name}.pdf', bbox_inches='tight', format='pdf')
    plt.savefig(f'{figure_dir}/{file_name}.png', bbox_inches='tight', format='png',
                        dpi=300, transparent=True)
