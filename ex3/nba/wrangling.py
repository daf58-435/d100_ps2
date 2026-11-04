# TODO: Find four interesting facts about the data and write a query to find the answer

"""
Fact 1: When was the longest period without a game?

1. game_dates - becomes a column contain each unique game date
2. gaps - becomes two columns [the previous game date and the next game date]
3. gap_lengths - casts the dates into numeric day values, does the difference 
                 and expresses it as a whole number
4. return the five longest gaps
"""

query_1 = """
WITH game_dates AS (
    SELECT DISTINCT DATE(game_date) AS game_day
    FROM game
    WHERE game_date IS NOT NULL
),
gaps AS (
    SELECT
        LAG(game_day) OVER (ORDER BY game_day) AS previous_game_date,
        game_day AS next_game_date
    FROM game_dates
),
gap_lengths AS (
    SELECT *,
        CAST(
            JULIANDAY(next_game_date) - JULIANDAY(previous_game_date)
            AS INTEGER
        ) - 1 AS days_without_games
    FROM gaps
    WHERE previous_game_date IS NOT NULL
)
SELECT *
FROM gap_lengths
ORDER BY days_without_games DESC, previous_game_date
LIMIT 5
"""

#which date had the most games in each year?

query_2 = """
WITH daily_counts AS (
    SELECT
        STRFTIME('%Y', game_date) AS year,
        DATE(game_date) AS game_day,
        COUNT(DISTINCT game_id) AS number_of_games
    FROM game
    WHERE game_date IS NOT NULL
    GROUP BY year, game_day
),
ranked_dates AS (
    SELECT *,
        DENSE_RANK() OVER (
            PARTITION BY year
            ORDER BY number_of_games DESC
        ) AS position
    FROM daily_counts
)
SELECT year, game_day, number_of_games
FROM ranked_dates
WHERE position = 1
ORDER BY year, game_day
"""

#which five years had the most games?

query_3 = """
WITH yearly_counts AS (
    SELECT
        STRFTIME('%Y', game_date) AS year,
        COUNT(DISTINCT game_id) AS number_of_games
    FROM game
    WHERE game_date IS NOT NULL
    GROUP BY year
)
SELECT *
FROM yearly_counts
ORDER BY number_of_games DESC, year
LIMIT 5
"""

# Average games for each month-day across the dataset's date range.
# Include zero-game days; February 29 is averaged over leap years only.

query_4 = """
WITH RECURSIVE
date_bounds AS (
    SELECT MIN(DATE(game_date)) AS first_day,
           MAX(DATE(game_date)) AS last_day
    FROM game
),
calendar(game_day) AS (
    SELECT first_day FROM date_bounds WHERE first_day IS NOT NULL
    UNION ALL
    SELECT DATE(game_day, '+1 day')
    FROM calendar, date_bounds
    WHERE game_day < last_day
),
daily_counts AS (
    SELECT
        DATE(game_date) AS game_day,
        COUNT(DISTINCT game_id) AS number_of_games
    FROM game
    WHERE game_date IS NOT NULL
    GROUP BY DATE(game_date)
)
SELECT
    STRFTIME('%m-%d', calendar.game_day) AS month_day,
    AVG(COALESCE(daily_counts.number_of_games, 0)) AS average_games,
    COUNT(*) AS years_observed
FROM calendar
LEFT JOIN daily_counts ON calendar.game_day = daily_counts.game_day
GROUP BY month_day
ORDER BY month_day
"""


