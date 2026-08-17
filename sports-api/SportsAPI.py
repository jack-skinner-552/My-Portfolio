# SportsAPI.py
import requests
from collections import defaultdict
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

from secret import API_KEY

TIMEZONE = "America/Denver"
LOCAL_TIMEZONE = ZoneInfo(TIMEZONE)

HEADERS = {
    "x-apisports-key": API_KEY
}

SPORTS = {
    "BASEBALL": {
        "url": "https://v1.baseball.api-sports.io/games",
    },
    "FOOTBALL": {
        "url": "https://v1.american-football.api-sports.io/games",
    },
    "BASKETBALL": {
        "url": "https://v1.basketball.api-sports.io/games",
        "nba_url": "https://v2.nba.api-sports.io/games",
    },
    "HOCKEY": {
        "url": "https://v1.hockey.api-sports.io/games",
    },
    "SOCCER": {
        "url": "https://v3.football.api-sports.io/fixtures",
    },
}

PREFERRED_LEAGUES = {
    "BASEBALL": (
        "MLB",
    ),
    "HOCKEY": (
        "NHL",
    ),
    "BASKETBALL": (
        "NBA",
        "NCAA",
        "NBA W",
        "NCAA Women",
    ),
    "FOOTBALL": (
        "NFL",
        "NCAA",
    ),
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


def parse_iso_timestamp(date_text: str | None) -> int | None:
    """Convert an ISO-8601 date string to a Unix timestamp."""

    if not date_text:
        return None

    try:
        parsed_date = datetime.fromisoformat(
            date_text.replace("Z", "+00:00")
        )
    except ValueError:
        return None

    if parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=timezone.utc)

    return int(parsed_date.timestamp())


def format_start_time(timestamp: int | str | None) -> str:
    """
    Convert a Unix timestamp to a readable time in America/Denver.

    Example:
        1785283500 -> 6:05 PM MDT
    """

    if timestamp in (None, ""):
        return "Time TBD"

    try:
        utc_time = datetime.fromtimestamp(
            int(timestamp),
            tz=timezone.utc,
        )
    except (TypeError, ValueError, OSError):
        return "Time TBD"

    local_time = utc_time.astimezone(LOCAL_TIMEZONE)

    # lstrip keeps this format compatible with Windows, where %-I
    # is not supported by strftime.
    return local_time.strftime(
        "%a %b %d, %I:%M %p %Z"
    ).replace(" 0", " ")


def get_game_timestamp(sport: str, game: dict) -> int | None:
    """Return the starting timestamp for a non-soccer game."""

    if sport == "FOOTBALL":
        return (
            game.get("game", {})
            .get("date", {})
            .get("timestamp")
        )

    return game.get("timestamp")


def get_game_status(sport: str, game: dict) -> str:
    """Return the short game status for a non-soccer game."""

    if sport == "FOOTBALL":
        return (
            game.get("game", {})
            .get("status", {})
            .get("short", "TBD")
        )

    return game.get("status", {}).get("short", "TBD")

def get_status_warning(
    timestamp: int | str | None,
    status: str,
) -> str:
    """Flag an API timestamp that conflicts with its game status."""

    if timestamp in (None, ""):
        return ""

    try:
        start_time = datetime.fromtimestamp(
            int(timestamp),
            tz=timezone.utc,
        ).astimezone(LOCAL_TIMEZONE)
    except (TypeError, ValueError, OSError):
        return ""

    current_time = datetime.now(LOCAL_TIMEZONE)

    if status == "FT" and start_time > current_time:
        return " [API schedule/status conflict]"

    return ""

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


def normalize_nba_game(game: dict) -> dict:
    """
    Convert an NBA API game into the same structure used by
    the general Basketball API.
    """

    nba_status = game.get("status", {})
    status_short = (
        nba_status.get("short")
        or nba_status.get("long")
        or "TBD"
    )

    return {
        "timestamp": parse_iso_timestamp(
            game.get("date", {}).get("start")
        ),
        "league": {
            "name": "NBA",
        },
        "teams": {
            "home": {
                "name": game["teams"]["home"]["name"],
            },
            "away": {
                "name": game["teams"]["visitors"]["name"],
            },
        },
        "status": {
            "short": status_short,
        },
        "scores": {
            "home": {
                "total": game["scores"]["home"]["points"],
            },
            "away": {
                "total": game["scores"]["visitors"]["points"],
            },
        },
    }


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


def get_basketball_games(game_date: date) -> list:
    """
    Retrieve games from both the general Basketball API
    and the dedicated NBA API.

    General basketball results are preserved even when the
    NBA endpoint returns zero games.
    """

    requested_date = game_date.isoformat()

    general_games = get_games(
        "BASKETBALL",
        game_date,
    )

    nba_games = request_api(
        sport="NBA",
        url=SPORTS["BASKETBALL"]["nba_url"],
        params={
            "date": requested_date,
        },
    )

    combined_games = []

    # Preserve all general Basketball API results except NBA,
    # because NBA comes from its dedicated endpoint.
    for game in general_games:
        league_name = (
            game.get("league", {})
            .get("name", "")
            .strip()
            .casefold()
        )

        if league_name != "nba":
            combined_games.append(game)

    for game in nba_games:
        combined_games.append(
            normalize_nba_game(game)
        )

    return combined_games


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
    """Print non-soccer games with their local starting times."""

    if not games:
        return

    write_line(f"\n===== {sport} =====")

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

        # Print each league's games in chronological order.
        sorted_games = sorted(
            leagues[league],
            key=lambda game: (
                get_game_timestamp(sport, game)
                if get_game_timestamp(sport, game) is not None
                else float("inf")
            ),
        )

        for game in sorted_games:
            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]
            status = get_game_status(sport, game)
            start_time = format_start_time(
                get_game_timestamp(sport, game)
            )

            if status in ("NS", "TBD"):
                write_line(
                    f"{start_time} | {away} @ {home} ({status})"
                )
                continue

            home_score = game["scores"]["home"]["total"]
            away_score = game["scores"]["away"]["total"]

            warning = get_status_warning(
                get_game_timestamp(sport, game),
                status,
            )

            write_line(
                f"{start_time} | "
                f"{away} {away_score} - "
                f"{home_score} {home} ({status})"
                f"{warning}"
            )


def print_soccer_games(games: list, write_line) -> None:
    """Print soccer matches with their local starting times."""

    if not games:
        return

    write_line("\n===== SOCCER =====")

    leagues = defaultdict(list)

    for game in games:
        league_name = game["league"]["name"]
        league_id = game["league"]["id"]
        country_name = game["league"].get("country", "Unknown")

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

        # Soccer stores its timestamp under fixture.timestamp.
        sorted_games = sorted(
            leagues[league_key],
            key=lambda game: (
                game.get("fixture", {}).get("timestamp")
                if game.get("fixture", {}).get("timestamp") is not None
                else float("inf")
            ),
        )

        for game in sorted_games:
            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]
            status = game["fixture"]["status"]["short"]
            start_time = format_start_time(
                game.get("fixture", {}).get("timestamp")
            )

            if status in ("NS", "TBD"):
                write_line(
                    f"{start_time} | {away} @ {home} ({status})"
                )
                continue

            home_score = game["goals"]["home"]
            away_score = game["goals"]["away"]

            warning = get_status_warning(
                get_game_timestamp("SOCCER", game),
                status,
            )

            write_line(
                f"{start_time} | "
                f"{away} {away_score} - "
                f"{home_score} {home} ({status})"
                f"{warning}"
            )


def run_sports_for_date(game_date: date, write_line) -> None:
    """Retrieve and print sports for the supplied date."""

    print_soccer_games(
        get_soccer_games(game_date),
        write_line,
    )

    print_games(
        "BASKETBALL",
        get_basketball_games(game_date),
        write_line,
    )

    if in_range(game_date, 4, 1, 10, 31):
        print_games(
            "BASEBALL",
            get_games("BASEBALL", game_date),
            write_line,
        )

    if in_range(game_date, 8, 1, 2, 14):
        print_games(
            "FOOTBALL",
            get_games("FOOTBALL", game_date),
            write_line,
        )

    if in_range(game_date, 10, 15, 6, 15):
        print_games(
            "HOCKEY",
            get_games("HOCKEY", game_date),
            write_line,
        )