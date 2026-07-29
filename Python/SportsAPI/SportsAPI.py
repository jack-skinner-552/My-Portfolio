# SportsAPI.py
import requests
from collections import defaultdict
from datetime import date

from secret import API_KEY

TIMEZONE = "America/Denver"

HEADERS = {
    "x-apisports-key": API_KEY
}

SPORTS = {
    "BASEBALL": {
        "url": "https://v1.baseball.api-sports.io/games",
    },
    "NFL": {
        "url": "https://v1.american-football.api-sports.io/games",
    },
    "BASKETBALL": {
        "url": "https://v1.basketball.api-sports.io/games",
    },
    "HOCKEY": {
        "url": "https://v1.hockey.api-sports.io/games",
    },
    "SOCCER": {
        "url": "https://v3.football.api-sports.io/fixtures",
    },
}

PREFERRED_LEAGUES = {
    "BASEBALL": ("MLB",),
    "HOCKEY": ("NHL",),
}

PREFERRED_SOCCER_LEAGUES = (
    {
        "name": "World Cup",
    },
    {
        "name": "World Cup - Women",
    },
    {
        "name": "Euro Championship",
    },
    {
        "name": "Premier League",
        "country": "England",
        "id": 39,
    },
    {
        "name": "Major League Soccer",
    },
    {
        "name": "NWSL Women",
    },
)


def in_range(
    current_date: date,
    start_month: int,
    start_day: int,
    end_month: int,
    end_day: int,
) -> bool:
    """Return whether a date is within a range that may cross years."""

    start = (start_month, start_day)
    end = (end_month, end_day)
    current = (current_date.month, current_date.day)

    if start <= end:
        return start <= current <= end

    return current >= start or current <= end


def request_api(
    sport: str,
    url: str,
    params: dict,
) -> list:
    """Send an API-Sports request and validate its JSON response."""

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    # Temporary diagnostic output
    print(f"{sport} request: {response.url}")
    print(f"{sport} results: {data.get('results')}")
    print(f"{sport} errors: {data.get('errors')}")

    api_errors = data.get("errors")

    if api_errors:
        raise RuntimeError(
            f"{sport} API returned an error: {api_errors}"
        )

    if "response" not in data:
        raise RuntimeError(
            f"{sport} API response did not contain a 'response' field: {data}"
        )

    return data["response"]


def get_games(sport: str, game_date: date) -> list:
    """Retrieve non-soccer games for the specified date."""

    requested_date = game_date.isoformat()

    return request_api(
        sport=sport,
        url=SPORTS[sport]["url"],
        params={
            "date": requested_date,
            "timezone": TIMEZONE,
        },
    )


def get_soccer_games(game_date: date) -> list:
    """Retrieve soccer matches for the specified date."""

    requested_date = game_date.isoformat()

    return request_api(
        sport="SOCCER",
        url=SPORTS["SOCCER"]["url"],
        params={
            "date": requested_date,
            "timezone": TIMEZONE,
        },
    )


def league_sort_key(sport: str, league: str) -> tuple:
    """
    Place preferred leagues first in their configured order,
    then sort all remaining leagues alphabetically.
    """

    preferred_leagues = PREFERRED_LEAGUES.get(sport, ())
    normalized_league = league.strip().casefold()

    for priority, preferred_league in enumerate(preferred_leagues):
        if normalized_league == preferred_league.strip().casefold():
            return priority, normalized_league

    return len(preferred_leagues), normalized_league

def soccer_league_sort_key(league_key: tuple) -> tuple:
    """
    Place preferred soccer leagues first.

    league_key contains:
        league name, country name, and league ID
    """

    league_name, country_name, league_id = league_key

    normalized_name = league_name.strip().casefold()
    normalized_country = country_name.strip().casefold()

    for priority, preferred in enumerate(PREFERRED_SOCCER_LEAGUES):
        preferred_name = preferred["name"].strip().casefold()

        if normalized_name != preferred_name:
            continue

        preferred_country = preferred.get("country")

        if (
            preferred_country
            and normalized_country != preferred_country.strip().casefold()
        ):
            continue

        preferred_id = preferred.get("id")

        if preferred_id is not None and league_id != preferred_id:
            continue

        return (
            priority,
            normalized_name,
            normalized_country,
        )

    return (
        len(PREFERRED_SOCCER_LEAGUES),
        normalized_name,
        normalized_country,
    )

def print_games(sport: str, games: list, write_line) -> None:
    """Print games for baseball, football, basketball, or hockey."""

    write_line(f"\n===== {sport} =====")

    if not games:
        write_line("No games today.")
        return

    leagues = defaultdict(list)

    for game in games:
        league = game["league"]["name"]
        leagues[league].append(game)

    sorted_leagues = sorted(
        leagues,
        key=lambda league: league_sort_key(sport, league),
    )

    for league in sorted_leagues:
        write_line(f"\n--- {league} ---")

        for game in leagues[league]:
            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]
            status = game["status"]["short"]

            if status in ("NS", "TBD"):
                write_line(f"{away} @ {home} ({status})")
                continue

            home_score = game["scores"]["home"]["total"]
            away_score = game["scores"]["away"]["total"]

            write_line(
                f"{away} {away_score} - "
                f"{home_score} {home} ({status})"
            )


def print_soccer_games(games: list, write_line) -> None:
    """Print soccer matches grouped by league and country."""

    write_line("\n===== SOCCER =====")

    if not games:
        write_line("No matches today.")
        return

    leagues = defaultdict(list)

    for game in games:
        league_name = game["league"]["name"]
        league_id = game["league"]["id"]
        country_name = game["league"].get("country", "Unknown")

        # A composite key prevents leagues with identical names
        # from being combined.
        league_key = (
            league_name,
            country_name,
            league_id,
        )

        leagues[league_key].append(game)

    sorted_leagues = sorted(
        leagues,
        key=soccer_league_sort_key,
    )

    for league_key in sorted_leagues:
        league_name, country_name, league_id = league_key

        write_line(
            f"\n--- {league_name} ({country_name}) ---"
        )

        for game in leagues[league_key]:
            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]
            status = game["fixture"]["status"]["short"]

            if status in ("NS", "TBD"):
                write_line(f"{away} @ {home} ({status})")
                continue

            home_score = game["goals"]["home"]
            away_score = game["goals"]["away"]

            write_line(
                f"{away} {away_score} - "
                f"{home_score} {home} ({status})"
            )


def run_sports_for_date(game_date: date, write_line) -> None:
    """Retrieve and print sports for the supplied date."""

    print_soccer_games(
        get_soccer_games(game_date),
        write_line,
    )

    if in_range(game_date, 4, 1, 10, 31):
        print_games(
            "BASEBALL",
            get_games("BASEBALL", game_date),
            write_line,
        )

    if in_range(game_date, 9, 15, 2, 7):
        print_games(
            "NFL",
            get_games("NFL", game_date),
            write_line,
        )

    if in_range(game_date, 10, 15, 6, 15):
        print_games(
            "BASKETBALL",
            get_games("BASKETBALL", game_date),
            write_line,
        )

        print_games(
            "HOCKEY",
            get_games("HOCKEY", game_date),
            write_line,
        )