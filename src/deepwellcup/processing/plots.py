"""Functions for creating plots"""
import os

import matplotlib.pyplot as plt  # type: ignore[import-untyped]
import pandas as pd
from matplotlib import patches, rc

from . import dirs
from .database_new import DataBase
from .points import RoundPoints
from .points_systems import points_system
from .round_data import RoundData

# set font to look like Latex
font = {"family": "serif", "size": 12}
rc("font", **font)


class Plots:  # pylint: disable=R0902
    """Class for creating plots"""

    def __init__(  # pylint: disable=R0913
        self,
        year,
        database: DataBase,
        max_round=4,
        plot_champions=True,
        save=False,
        show=False,
    ):
        self.year = year
        self.max_round = max_round
        self.plot_champions = plot_champions
        self.save = save
        self.show = show
        self._database = database
        self._points_system = points_system(year)
        self._total_points = self._create_table("total")
        self._other_points = self._create_table("other")
        self._figure = plt.figure(figsize=(8, 0.5 * len(self.individuals)))
        self._axis = self.figure.add_subplot(111)
        self._axis_list: list = []
        self._patch = None

    @property
    def figure(self):
        """Figure handle"""
        return self._figure

    @property
    def axis(self):
        """Axis handle"""
        return self._axis

    def close(self):
        """Close the figure"""
        return plt.close(self.figure)

    @property
    def individuals(self):
        """List of individuals"""
        return self.total_points.columns.to_list()

    @property
    def total_points(self):
        """Total Points"""
        return self._total_points

    @property
    def other_points(self):
        """Other Points"""
        return self._other_points

    @property
    def _max_points(self):
        """Maximum total Points"""
        return self.total_points.loc["Total"].max()

    @property
    def _colors(self):
        """Colors to use in bar chart"""
        round_colors = [
            "#B87D63",
            "#95c4e8",
            "#a3e6be",
            "#fbee9d",
            "#fbbf9d",
            "#e29dfb",
        ]
        return dict(zip(self._round_names.values(), round_colors))

    @property
    def _round_names(self):
        """Dictionary of the names for each round from the round number"""
        return {
            "Q": "Round Q",
            1: "Round 1",
            2: "Round 2",
            3: "Round 3",
            4: "Round 4",
            "Champions": "Champions",
        }

    @property
    def rounds_to_plot(self):
        """The list of rounds to be plotted"""
        if self.max_round == "Q":
            end = 1
        elif self.max_round == 4 and self.plot_champions:
            end = 6
        else:
            end = self.max_round + 1
        start = 1 if self.year != 2020 else 0
        indices = slice(start, end)
        rounds_to_keep = dict(list(self._round_names.items())[indices])
        if (
            self.max_round == 3
            and self.plot_champions
            and "stanley_cup_finalist" in self._points_system
        ):
            rounds_to_keep["Champions"] = "Champions"
        return rounds_to_keep

    def _add_column_to_table(self, rnd, category):
        """Modify Series to be the appropriate structure for making a Dataframe."""
        round_data = RoundData(self.year, rnd, self._database)
        points = RoundPoints(round_data)
        column = getattr(points, category)
        if column is None:
            return pd.Series(name=self.rounds_to_plot[rnd], dtype="int64")
        if category == "other":
            column.name = self.rounds_to_plot[rnd]
        return column

    def _create_table(self, category):
        """Create a table of values for a category for each individual"""
        all_round_series = [
            self._add_column_to_table(rnd, category)
            for rnd in self.rounds_to_plot.keys()
        ]
        df = pd.concat(all_round_series, axis=1).transpose()
        total = df.sum().rename("Total").to_frame().transpose()
        df_with_total = pd.concat([df, total])
        return (
            df_with_total.rename_axis(columns="Individuals")
            .astype("Int64")
            .sort_values(
                by=["Total", "Individuals"], axis="columns", ascending=[True, False]
            )
        )

    def standings(self):
        """Create a bar chart of the points standings in a year"""

        self._create_barchart()

        # modify axis lines and ticks
        self.axis.set_yticks(range(len(self.individuals)))
        self.axis.set_yticklabels(self.individuals)
        self.axis.set_xlim(0, self._max_points * 1.02)
        self.axis.spines["right"].set_visible(False)
        self.axis.spines["bottom"].set_visible(False)
        self.axis.spines["top"].set_visible(False)
        self.axis.yaxis.set_ticks_position("none")
        self.axis.xaxis.set_ticks_position("none")
        self.axis.get_xaxis().set_ticks([])
        # figure title
        fig_title = f"Points - {self.year} - Round {self.max_round}"
        if not self.plot_champions:
            fig_title += " - no Champions"
        self.axis.set_title(fig_title)

        self._add_legend()

        if self.save:
            self._save_figure()

        if self.show:
            plt.show(block=False)

    def _create_barchart(self):
        for individual_index, individual in enumerate(self.individuals):
            left_end = 0
            for playoff_round in self.rounds_to_plot.values():
                round_points = self.total_points[individual][playoff_round]
                if not pd.isna(round_points):
                    self._patch = self.axis.barh(
                        individual_index,
                        round_points,
                        left=left_end,
                        align="center",
                        edgecolor="black",
                        color=self._colors[playoff_round],
                        label=playoff_round,
                    )
                    if playoff_round not in [
                        item.get_label() for item in self._axis_list
                    ]:
                        self._axis_list.append(self._patch)
                    self._add_round_point_text(individual, round_points, playoff_round)
                    left_end += round_points
            self._add_total_point_text(individual, individual_index, left_end)

    def _text_location(self):
        """Position to place the string within the stacked bar"""
        patch = self._patch[0]
        patch_horizontal_center = patch.get_x() + patch.get_width() / 2
        patch_vertical_center = patch.get_y() + patch.get_height() / 2
        return patch_horizontal_center, patch_vertical_center

    def _add_round_point_text(self, individual, round_points, playoff_round):
        """Add string of the points earned by the individual in a playoff round"""

        # find position to place the string
        patch_horizontal_center, patch_vertical_center = self._text_location()

        # create the string
        point_string = f"{round_points}"
        if (
            playoff_round != "Champions"
            and individual in self.other_points.columns
            and not pd.isna(self._other_points[individual][playoff_round])
        ):
            if self.year == 2009:
                point_string += "$\\ast$"
            elif self.year == 2015:
                point_string += "$\\dagger$"

        self._add_text([patch_horizontal_center, patch_vertical_center], point_string)

    def _add_total_point_text(self, individual, individual_index, left_end):
        """Add string of the points earned by the individual in the year"""
        horizontal_position = left_end + self._max_points / 25
        total_points = self.total_points[individual]["Total"]
        self._add_text([horizontal_position, individual_index], f"{total_points}")

    def _add_text(self, position, text):
        """Add text to figure"""
        # potentially look into pyplot.bar_label
        self.axis.text(position[0], position[1], text, ha="center", va="center")

    def _add_legend(self):
        """Add the legend"""

        # reorder the handles
        round_list = [item.get_label() for item in self._axis_list]
        correct_list = sorted(round_list)
        if "Champions" in correct_list:
            # move 'Champions' to the end of the list
            correct_list.remove("Champions")
            correct_list.append("Champions")
        if "Round Q" in correct_list:
            # move 'Round Q' to the start of the list
            correct_list.remove("Round Q")
            correct_list = ["Round Q"] + correct_list
        index_order = [round_list.index(round) for round in correct_list]
        ordered_handles = [self._axis_list[i] for i in index_order]

        if len(self.other_points.columns) > 0:
            if self.year == 2009:
                label = "$\\ast$: -7 points"
            elif self.year == 2015:
                label = "$\\dagger$: 50 points given"
            ordered_handles.append(
                patches.Rectangle(
                    (0, 0),
                    1,
                    1,
                    facecolor="none",
                    fill=False,
                    edgecolor="none",
                    linewidth=0,
                    label=label,
                )
            )

        # Put a legend to the right of the current axis
        plt.legend(
            handles=ordered_handles, loc="center left", bbox_to_anchor=(1.05, 0.5)
        )

    def _save_figure(self):
        """Save figure to disk"""
        # file_name = self.axis.get_title()
        file_name = self.axis.get_title().replace(" ", "")
        figure_dir = dirs.year_figures(self.year)
        if not os.path.exists(figure_dir):
            os.mkdir(figure_dir)
        plt.savefig(f"{figure_dir}/{file_name}.pdf", bbox_inches="tight", format="pdf")
        plt.savefig(
            f"{figure_dir}/{file_name}.png",
            bbox_inches="tight",
            format="png",
            dpi=300,
            transparent=True,
        )
