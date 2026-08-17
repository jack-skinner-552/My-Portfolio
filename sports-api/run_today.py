# run_today.py
from datetime import date, datetime
from pathlib import Path

from SportsAPI import run_sports_for_date


OUTPUT_DIR = Path("output")


def main() -> None:
    today = date.today()
    today_str = today.isoformat()
    run_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log_path = OUTPUT_DIR / f"sports_games_{today_str}.txt"

    # Append each run to the current day's file.
    with log_path.open("a", encoding="utf-8") as log_file:

        def write_line(text: str = "") -> None:
            print(text)
            log_file.write(text + "\n")

        write_line("=" * 50)
        write_line(f"Sports API Run Time: {run_time}")
        write_line(f"Fetching games for: {today_str}")
        write_line("=" * 50)
        write_line()

        try:
            run_sports_for_date(today, write_line)
        except Exception as error:
            write_line(f"\nError retrieving sports data: {error}")
            raise

        write_line()
        write_line("=" * 50)


if __name__ == "__main__":
    main()