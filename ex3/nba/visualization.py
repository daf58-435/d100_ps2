"""Plot the DataFrames returned by the four NBA fact queries."""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_longest_gap(data, ax=None):
    """Plot the number of full days between each pair of recorded game dates."""
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 4))

    labels = (
        data["previous_game_date"].astype(str)
        + " to "
        + data["next_game_date"].astype(str)
    )
    bars = ax.barh(range(len(data)), data["days_without_games"], color="steelblue")
    ax.set_yticks(range(len(data)), labels=labels)
    ax.invert_yaxis()
    ax.bar_label(bars, padding=4)
    ax.margins(x=0.15)
    ax.set_xlabel("Full days without recorded games")
    ax.set_title("Five longest gaps in the dataset")
    return ax


def plot_game_counts(data, x_column, title, ax=None):
    """Plot game counts by year, date, or month-day; return the plot's Axes."""
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))

    # Use positions so repeated labels still get separate bars.
    bars = ax.bar(
        range(len(data)), data["number_of_games"], color="steelblue"
    )
    ax.set_xticks(
        range(len(data)), labels=data[x_column].astype(str), rotation=60
    )
    if len(data) <= 10:
        ax.bar_label(bars, padding=3)
    ax.margins(y=0.15)
    ax.set_xlabel(x_column.replace("_", " ").capitalize())
    ax.set_ylabel("Number of games")
    ax.set_title(title)
    return ax


def plot_average_games(data, ax=None):
    """Plot average recorded games by month-day, including February 29."""
    if ax is None:
        _, ax = plt.subplots(figsize=(12, 4))

    data = data.sort_values("month_day")
    # A leap year supplies an x-axis position for every possible month-day.
    dates = pd.to_datetime("2000-" + data["month_day"])
    ax.plot(dates, data["average_games"], color="steelblue", linewidth=1.5)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlim(pd.Timestamp("2000-01-01"), pd.Timestamp("2000-12-31"))
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Day of the calendar year")
    ax.set_ylabel("Average games per day")
    ax.set_title("Average recorded games on each calendar day")
    ax.grid(axis="y", alpha=0.25)
    return ax


def plot_results(results):
    """Plot results[1] through results[4] and return (figure, axes).

    For question 2, show one maximum daily count per year. The input
    DataFrames retain all tied dates and are not modified.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), layout="constrained")
    plot_longest_gap(results[1], ax=axes[0, 0])

    busiest = results[2].groupby("year")["number_of_games"].max().sort_index()
    axes[0, 1].plot(pd.to_numeric(busiest.index), busiest.values)
    axes[0, 1].set_title("Most games on a single day in each year")
    axes[0, 1].set_xlabel("Calendar year")
    axes[0, 1].set_ylabel("Games on the busiest day")

    plot_game_counts(
        results[3], "year", "Five calendar years with the most games", ax=axes[1, 0]
    )
    plot_average_games(results[4], ax=axes[1, 1])
    return fig, axes
