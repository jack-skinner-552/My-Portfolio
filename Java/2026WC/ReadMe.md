# FIFA World Cup 2026 Java Tracker

A Java application that fetches and displays live FIFA World Cup 2026 data, including match schedules, live scores, group standings, and team information. The project demonstrates REST API integration, JSON parsing with Jackson, time zone handling, and formatted console reporting.

---

## Features:

### Match Reporting

- Displays all matches scheduled for the current day
- Sorts matches chronologically (earliest → latest)
- Shows:
  - Home and away teams
  - Current scores
  - Match status (LIVE, FINISHED, UPCOMING)
  - Stadium name and location
  - Goal scorers when available
- Converts kickoff times to the user's local time zone

### Group Standings
- Displays World Cup group standings
- Teams automatically resolved from Team IDs
- Groups sorted alphabetically (A → L)
- Teams sorted by points descending
- Empty groups automatically hidden

### Report Generation
- Outputs report to console
- Saves report as a timestamped text file

Example filename:  
`WorldCupReport_2026-06-16_14-30.txt`

### API Reliability
* Automatic retry handling
* SSL handshake failure recovery
* HTTP 500 retry support
* Network interruption recovery
* Progressive retry delays between attempts

### Progress Tracking
* Console progress bar displays API retrieval status

Example:

    [██████--------------] 33% - Games Retrieved.
    [█████████████-------] 66% - Groups Retrieved.
    [████████████████████]100% - Teams Retrieved.

### Graceful Failure Handling

If one API endpoint fails:

* Available data is still displayed
* Partial reports are generated
* Application does not terminate unnecessarily

---

## Technologies Used

- Java 17
- Java HttpClient (java.net.http)
- Jackson Databind (JSON parsing)
- Java Time API (LocalDate, ZonedDateTime)
- Maven (dependency management)

---

## API Used

This project uses the World Cup 2026 API provided by:

**[reza rahiminia](https://github.com/rezarahiminia/worldcup2026)**

Base endpoints:
- https://worldcup26.ir/get/games
- https://worldcup26.ir/get/groups
- https://worldcup26.ir/get/teams

---

## Project Structure

    src/  
    ├── api/  
    │    └── FootballApiClient.java  
    ├── model/  
    │    ├── Match.java  
    │    ├── Group.java  
    │    ├── GroupTeam.java  
    │    ├── Team.java  
    │    ├── TeamsResponse.java  
    │    ├── GroupsResponse.java  
    │    └── GamesResponse.java  
    └── Main.java

---

## Key Features Explained

### Match Status Logic
Matches are classified as:
- FINISHED → match marked complete by API
- LIVE → score has changed OR kickoff time has passed
- UPCOMING → scheduled kickoff time not reached

### Group Standings
- Groups are sorted alphabetically (A → L)
- Teams are sorted by points descending
- Empty groups (all zeros) are hidden

### Time Conversion
Kickoff times are converted from stadium local time to system time zone.

---

## Error Handling

The API client includes retry logic for:
- SSLHandshakeException
- IOException
- HTTP 500 Internal Server Error

Default retry configuration:

* 3 attempts
* Increasing delay between retries
* Graceful fallback behavior
---

## Example Output

    FIFA World Cup 2026 Daily Report
    June 22, 2026
    10:55 MDT
    
    =====================================
    
    MATCHES TODAY
    GROUP MATCH
    Argentina 0 - 0 Austria
    Kickoff: 06 22, 2026 11:00 AM MDT
    AT&T Stadium
    Arlington, TX
    
    
    -------------------------------------
    
    GROUP MATCH
    France 0 - 0 Iraq
    Kickoff: 06 22, 2026 3:00 PM MDT
    Lincoln Financial Field
    Philadelphia, PN
    
    
    -------------------------------------
    
    GROUP MATCH
    Norway 0 - 0 Senegal
    Kickoff: 06 22, 2026 6:00 PM MDT
    MetLife Stadium
    East Rutherford, NJ
    
    
    -------------------------------------
    
    GROUP MATCH
    Jordan 0 - 0 Algeria
    Kickoff: 06 22, 2026 9:00 PM MDT
    Levi's Stadium
    Santa Clara, CA
    
    
    -------------------------------------
    
    
    GROUP STANDINGS (RECALCULATED)
    ================================
    
    GROUP H
    Team                           MP  W  D  L Pts GD
    Spain                           2  1  1  0   4  4
    Uruguay                         2  0  2  0   2  0
    Cape Verde                      2  0  2  0   2  0
    Saudi Arabia                    2  0  1  1   1 -4
    
    GROUP I
    Team                           MP  W  D  L Pts GD
    Norway                          1  1  0  0   3  3
    France                          1  1  0  0   3  2
    Senegal                         1  0  0  1   0 -2
    Iraq                            1  0  0  1   0 -3
    
    GROUP D
    Team                           MP  W  D  L Pts GD
    United States                   2  2  0  0   6  5
    Australia                       2  1  0  1   3  0
    Paraguay                        2  1  0  1   3 -2
    Turkey                          2  0  0  2   0 -3
    
    GROUP E
    Team                           MP  W  D  L Pts GD
    Germany                         2  2  0  0   6  7
    Ivory Coast                     2  1  0  1   3  0
    Ecuador                         2  0  1  1   1 -1
    Curaçao                         2  0  1  1   1 -6
    
    GROUP F
    Team                           MP  W  D  L Pts GD
    Netherlands                     2  1  1  0   4  4
    Japan                           2  1  1  0   4  4
    Sweden                          2  1  0  1   3  0
    Tunisia                         2  0  0  2   0 -8
    
    GROUP G
    Team                           MP  W  D  L Pts GD
    Egypt                           2  1  1  0   4  2
    Iran                            2  0  2  0   2  0
    Belgium                         2  0  2  0   2  0
    New Zealand                     2  0  1  1   1 -2
    
    GROUP A
    Team                           MP  W  D  L Pts GD
    Mexico                          2  2  0  0   6  3
    South Korea                     2  1  0  1   3  0
    Czech Republic                  2  0  1  1   1 -1
    South Africa                    2  0  1  1   1 -2
    
    GROUP B
    Team                           MP  W  D  L Pts GD
    Canada                          2  1  1  0   4  6
    Switzerland                     2  1  1  0   4  3
    Bosnia and Herzegovina          2  0  1  1   1 -3
    Qatar                           2  0  1  1   1 -6
    
    GROUP L
    Team                           MP  W  D  L Pts GD
    England                         1  1  0  0   3  2
    Ghana                           1  1  0  0   3  1
    Panama                          1  0  0  1   0 -1
    Croatia                         1  0  0  1   0 -2
    
    GROUP K
    Team                           MP  W  D  L Pts GD
    Colombia                        1  1  0  0   3  2
    Portugal                        1  0  1  0   1  0
    Democratic Republic of the Congo  1  0  1  0   1  0
    Uzbekistan                      1  0  0  1   0 -2
    
    GROUP C
    Team                           MP  W  D  L Pts GD
    Brazil                          2  1  1  0   4  3
    Morocco                         2  1  1  0   4  1
    Scotland                        2  1  0  1   3  0
    Haiti                           2  0  0  2   0 -4
    
    GROUP J
    Team                           MP  W  D  L Pts GD
    Argentina                       1  1  0  0   3  3
    Austria                         1  1  0  0   3  2
    Jordan                          1  0  0  1   0 -2
    Algeria                         1  0  0  1   0 -3
    
    TEAMS ADVANCING IF THE WORLD CUP ENDED TODAY
    ===========================================
    
    GROUP H
    1. Spain                     Pts: 4 GD:  4
       2. Cape Verde                Pts: 2 GD:  0
    
    GROUP I
    1. France                    Pts: 3 GD:  2
       2. Norway                    Pts: 3 GD:  3
    
    GROUP D
    1. United States             Pts: 6 GD:  5
       2. Paraguay                  Pts: 3 GD: -2
    
    GROUP E
    1. Germany                   Pts: 6 GD:  7
       2. Ivory Coast               Pts: 3 GD:  0
    
    GROUP F
    1. Japan                     Pts: 4 GD:  4
       2. Netherlands               Pts: 4 GD:  4
    
    GROUP G
    1. Egypt                     Pts: 4 GD:  2
       2. Belgium                   Pts: 2 GD:  0
    
    GROUP A
    1. Mexico                    Pts: 6 GD:  3
       2. South Korea               Pts: 3 GD:  0
    
    GROUP B
    1. Switzerland               Pts: 4 GD:  3
       2. Canada                    Pts: 4 GD:  6
    
    GROUP L
    1. Ghana                     Pts: 3 GD:  1
       2. England                   Pts: 3 GD:  2
    
    GROUP K
    1. Colombia                  Pts: 3 GD:  2
       2. Portugal                  Pts: 1 GD:  0
    
    GROUP C
    1. Morocco                   Pts: 4 GD:  1
       2. Brazil                    Pts: 4 GD:  3
    
    GROUP J
    1. Austria                   Pts: 3 GD:  2
       2. Argentina                 Pts: 3 GD:  3
    
    TOP 8 THIRD-PLACE TEAMS
    If the World Cup ended today, these teams would also advance.
    ===========================================================
    1. Sweden                    Pts: 3 GD:  0 GF: 6
       2. Australia                 Pts: 3 GD:  0 GF: 2
       3. Scotland                  Pts: 3 GD:  0 GF: 1
       4. Uruguay                   Pts: 2 GD:  0 GF: 3
       5. Iran                      Pts: 2 GD:  0 GF: 2
       6. Democratic Republic of the Congo Pts: 1 GD:  0 GF: 1
       7. South Africa              Pts: 1 GD: -2 GF: 1
       8. Curaçao                   Pts: 1 GD: -6 GF: 1
    
    ELIMINATED IF WORLD CUP ENDED TODAY
    ===================================
    
    Bottom Third-Place Teams
    ------------------------
    Qatar                     Pts: 1 GD: -6 GF: 1
    Croatia                   Pts: 0 GD: -2 GF: 2
    Iraq                      Pts: 0 GD: -3 GF: 1
    Algeria                   Pts: 0 GD: -3 GF: 0
    
    Fourth-Place Teams
    ------------------
    Group H  Saudi Arabia              Pts: 1 GD: -4 GF: 1
    Group I  Senegal                   Pts: 0 GD: -2 GF: 1
    Group D  Turkey                    Pts: 0 GD: -3 GF: 0
    Group E  Ecuador                   Pts: 1 GD: -1 GF: 0
    Group F  Tunisia                   Pts: 0 GD: -8 GF: 1
    Group G  New Zealand               Pts: 1 GD: -2 GF: 3
    Group A  Czech Republic            Pts: 1 GD: -1 GF: 2
    Group B  Bosnia and Herzegovina    Pts: 1 GD: -3 GF: 2
    Group L  Panama                    Pts: 0 GD: -1 GF: 0
    Group K  Uzbekistan                Pts: 0 GD: -2 GF: 1
    Group C  Haiti                     Pts: 0 GD: -4 GF: 0
    Group J  Jordan                    Pts: 0 GD: -2 GF: 1
---

## Future Improvements

* GUI application using JavaFX
* Web dashboard using Spring Boot
* Automated scheduled report generation

---

## Credits

World Cup 2026 API

Created and maintained by Reza Rahiminia

GitHub:
https://github.com/rezarahiminia/worldcup2026

API:
https://worldcup26.ir/

---

## License

This project is for educational purposes.
