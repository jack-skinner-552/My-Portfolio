# SportsAPI

SportsAPI is a Python command-line project that retrieves daily schedules and scores from API-Sports for:

- Soccer
- Baseball
- American football
- Basketball
- Hockey

The project can retrieve games for the current date or for a date supplied through the command line. Results are printed to the terminal and appended to a dated text file in the `output` directory.

## Features

- Retrieves schedules and scores from multiple API-Sports endpoints.
- Uses the `America/Denver` timezone for API requests.
- Groups games by league.
- Places preferred leagues at the top of each section.
- Separates soccer leagues with identical names by country and league ID.
- Runs only sports that are likely to be in season.
- Supports current-day and custom-date commands.
- Validates the limited date range available to free-tier API accounts.
- Provides a `--paid` option to skip local free-tier validation.
- Logs API results and errors for easier troubleshooting.

## Preferred League Order

### Baseball

1. MLB
2. All remaining leagues alphabetically

### Hockey

1. NHL
2. All remaining leagues alphabetically

### Soccer

When games are available, these leagues are placed first in this order:

1. World Cup
2. World Cup - Women
3. Euro Championship
4. Premier League — England, league ID `39`
5. Major League Soccer
6. NWSL Women

All remaining soccer leagues are sorted alphabetically by league and country.

## Project Structure

```text
SportsAPI/
├── SportsAPI.py
├── run_today.py
├── run_for_date.py
├── secret.py
├── output/
├── requirements.txt
└── README.md
```

### File Responsibilities

- `SportsAPI.py` contains the API endpoints, request handling, sorting, formatting, seasonal checks, and reusable sports functions.
- `run_today.py` retrieves games for the current local date.
- `run_for_date.py` retrieves games for a date provided as a command-line argument.
- `secret.py` stores the API-Sports key locally.
- `output/` contains dated text output files.

## Requirements

- Python 3.10 or newer
- An API-Sports account and API key
- The `requests` Python package

## Installation

### 1. Clone or download the project

```powershell
git clone <repository-url>
cd SportsAPI
```

Replace `<repository-url>` with the URL of your repository.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```powershell
python -m pip install requests
```

A minimal `requirements.txt` can contain:

```text
requests
```

Install from it with:

```powershell
python -m pip install -r requirements.txt
```

## API Key Configuration

Create `secret.py` in the project root:

```python
API_KEY = "your-api-sports-key"
```

Do not commit `secret.py` to Git.

Add the following entries to `.gitignore`:

```gitignore
.venv/
__pycache__/
secret.py
output/
```

Because an API key was previously exposed during development, rotate it before publishing the repository.

## Usage

### Retrieve games for today

```powershell
python .\run_today.py
```

The script:

1. Uses the current local date.
2. Retrieves games for sports considered in season.
3. Prints the results in the terminal.
4. Appends the results to a dated file.

Example output file:

```text
output/sports_games_2026-07-28.txt
```

### Retrieve games for a specified date

Use a date in `YYYY-MM-DD` format:

```powershell
python .\run_for_date.py 2026-07-28
```

An invalid format produces an argument error:

```powershell
python .\run_for_date.py 07-28-2026
```

### Paid-plan mode

The free API plan restricts access to a small date window based on the API's UTC date. To skip the script's local free-tier validation, pass `--paid`:

```powershell
python .\run_for_date.py 2026-07-19 --paid
```

The `--paid` option only skips validation inside `run_for_date.py`. API-Sports will still reject the request unless the API key itself has access to the requested date.

## Free-Tier Date Window

`run_for_date.py` calculates the free-tier range using UTC:

```text
API UTC date - 1 day
through
API UTC date + 1 day
```

This may differ from the current date in Mountain Time.

For example, after 6:00 PM MDT during daylight saving time, UTC has already advanced to the next calendar day. A date that is locally “yesterday” may therefore be outside the API's permitted range.

When a date is outside the calculated range, the script displays an error before making API requests.

## Seasonal Sports Logic

Soccer runs year-round.

The other sports run during these configured date ranges:

| Sport | Configured range |
|---|---|
| Baseball | April 1 through October 31 |
| American football | September 15 through February 7 |
| Basketball | October 15 through June 15 |
| Hockey | October 15 through June 15 |

The `in_range()` helper supports seasons that cross from one calendar year into the next.

These ranges control whether the project requests a sport. They are general scheduling ranges rather than guarantees that every league has games on every date.

## Output Format

Each execution writes a header containing the run time and requested date:

```text
==================================================
Sports API Run Time: 2026-07-28 06:32:36 PM
Fetching games for: 2026-07-28
==================================================
```

Games are grouped by sport and league:

```text
===== BASEBALL =====

--- MLB ---
Colorado Rockies @ San Diego Padres (NS)
Cleveland Guardians 6 - 5 Cincinnati Reds (FT)
```

Common status codes include:

| Status | Meaning |
|---|---|
| `NS` | Not started |
| `TBD` | Time or status to be determined |
| `FT` | Finished |
| `POST` | Postponed |
| `CANC` | Cancelled |
| `IN1`–`IN9` | Baseball game in progress |
| `HT` | Soccer halftime |
| `1H` / `2H` | Soccer first or second half |
| `AET` | Finished after extra time |
| `PEN` | Finished after penalties |

The project prints raw status codes returned by API-Sports.

## API Diagnostics

`SportsAPI.py` currently prints diagnostic information for every request:

```text
SOCCER request: https://v3.football.api-sports.io/fixtures?date=...
SOCCER results: 25
SOCCER errors: {}
```

These lines help identify:

- Incorrect dates
- Free-plan restrictions
- Invalid API keys
- Quota limits
- Endpoint errors
- Empty API responses

To disable these messages later, remove or comment out the diagnostic `print()` calls in `request_api()`.

## Error Handling

The project checks for:

- HTTP request failures
- API-Sports errors returned inside otherwise successful HTTP responses
- Missing `response` fields
- Invalid command-line date formats
- Dates outside the calculated free-tier window

Example plan error:

```text
SOCCER API returned an error:
{'plan': 'Free plans do not have access to this date...'}
```

## Troubleshooting

### Python cannot find the script

Run the command from the project root:

```powershell
cd C:\Users\<username>\PycharmProjects\SportsAPI
dir *.py
```

The project source files should be beside `secret.py`, not inside `.venv`.

Expected files:

```text
SportsAPI.py
run_today.py
run_for_date.py
secret.py
```

### `ModuleNotFoundError: No module named 'requests'`

Activate the virtual environment and install the package:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install requests
```

### `ModuleNotFoundError: No module named 'secret'`

Confirm that `secret.py` is in the same project directory as `SportsAPI.py`.

### `ModuleNotFoundError: No module named 'SportsAPI'`

Confirm the filename and import capitalization match:

```python
from SportsAPI import run_sports_for_date
```

On case-sensitive operating systems, `SportsAPI.py` and `sportsapi.py` are different filenames.

### No games are returned

Check the diagnostic output:

```text
SPORT results: 0
SPORT errors: {}
```

This means the API accepted the request but returned no games.

If the error contains a `plan` entry, the requested date is outside the API token's permitted range.

### Duplicate output

Output files are opened in append mode. Running the script multiple times on the same date adds another complete report to the same file.

To replace the file each time, change:

```python
log_path.open("a", encoding="utf-8")
```

to:

```python
log_path.open("w", encoding="utf-8")
```

## Possible Future Improvements

- Add command-line options for selecting individual sports.
- Add JSON or CSV output.
- Sort games within a league by start time.
- Replace `secret.py` with environment variables.
- Add automated tests for date-range and sorting functions.
- Add retry handling for temporary API failures.
- Add structured logging instead of diagnostic `print()` statements.
- Use exact league IDs for every preferred soccer league.
- Package the project as an installable command-line application.

## Security Notes

Never publish an active API key in:

- Source code
- README examples
- Screenshots
- Terminal output
- Git commit history

If a key is accidentally committed, remove it from the repository, rotate it through API-Sports, and use the replacement key only in `secret.py` or an environment variable.

## License

Add the license that applies to your repository. For example, create a `LICENSE` file if you plan to release the project under the MIT License.
