# run_for_date.py
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from SportsAPI import run_sports_for_date


OUTPUT_DIR = Path("output")


def parse_date(date_text: str):
    """Convert a YYYY-MM-DD string into a date object."""

    try:
        return datetime.strptime(date_text, "%Y-%m-%d").date()
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"Invalid date: {date_text}. Use YYYY-MM-DD."
        ) from error


def get_free_tier_date_range():
    """Return the API-Sports free-tier date range based on UTC."""

    api_today = datetime.now(timezone.utc).date()
    earliest_date = api_today - timedelta(days=1)
    latest_date = api_today + timedelta(days=1)

    return api_today, earliest_date, latest_date


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Retrieve sports games for a specified date."
    )

    parser.add_argument(
        "date",
        type=parse_date,
        help="Date to retrieve in YYYY-MM-DD format",
    )

    parser.add_argument(
        "--paid",
        action="store_true",
        help="Skip free-tier date validation for a paid API plan",
    )

    args = parser.parse_args()

    game_date = args.date
    paid_plan = args.paid

    api_today, earliest_date, latest_date = get_free_tier_date_range()

    # Only enforce the restricted date range for free-tier users.
    if not paid_plan and not earliest_date <= game_date <= latest_date:
        parser.error(
            f"The free API tier only supports dates from "
            f"{earliest_date} through {latest_date}. "
            f"The API's current UTC date is {api_today}. "
            f"Use --paid to skip this validation."
        )

    date_string = game_date.isoformat()
    run_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log_path = OUTPUT_DIR / f"sports_games_{date_string}.txt"

    with log_path.open("a", encoding="utf-8") as log_file:

        def write_line(text: str = "") -> None:
            print(text)
            log_file.write(text + "\n")

        write_line("=" * 50)
        write_line(f"Sports API Run Time: {run_time}")
        write_line(f"Fetching games for: {date_string}")
        write_line(
            f"API plan validation: "
            f"{'Paid plan - skipped' if paid_plan else 'Free tier'}"
        )
        write_line("=" * 50)
        write_line()

        try:
            run_sports_for_date(game_date, write_line)
        except Exception as error:
            write_line(f"\nUnable to retrieve sports data: {error}")
            return

        write_line()
        write_line("=" * 50)

    print(f"\nResults saved to: {log_path}")


if __name__ == "__main__":
    main()