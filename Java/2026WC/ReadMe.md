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
    June 15, 2026  
    02:02 MDT
    =====================================
    
    MATCHES TODAY
    
    Spain 0 - 0 Cape Verde  
    Status: FINISHED  
    Mercedes-Benz Stadium  
    Atlanta, GA  
    
    -------------------------------------
    
    Belgium 0 - 1 Egypt
    Status: LIVE
    Lumen Field
    Seattle, WA
    
    -------------------------------------
    
    Saudi Arabia 0 - 0 Uruguay
    Kickoff: 06 15, 2026 4:00 PM MDT
    Hard Rock Stadium
    Miami, FL
    
    -------------------------------------
    
    Iran 0 - 0 New Zealand
    Kickoff: 06 15, 2026 7:00 PM MDT
    SoFi Stadium
    Los Angeles, CA
    
    -------------------------------------
    
    
    GROUP STANDINGS
    ==============================
    
    GROUP A
    Team                      MP  W  D  L Pts
    Mexico                     1  1  0  0   3
    South Korea                1  1  0  0   3
    South Africa               1  0  0  1   0
    Czech Republic             1  0  0  1   0
    
    GROUP B
    Team                      MP  W  D  L Pts
    Canada                     1  0  1  0   1
    Bosnia and Herzegovina     1  0  1  0   1
    Qatar                      1  0  1  0   1
    Switzerland                1  0  1  0   1
    
    GROUP C
    Team                      MP  W  D  L Pts
    Scotland                   1  1  0  0   3
    Brazil                     1  0  1  0   1
    Morocco                    1  0  1  0   1
    Haiti                      1  0  0  1   0
    
    GROUP D
    Team                      MP  W  D  L Pts
    United States              1  1  0  0   3
    Australia                  1  1  0  0   3
    Paraguay                   1  0  0  1   0
    Turkey                     1  0  0  1   0
    
    GROUP E
    Team                      MP  W  D  L Pts
    Germany                    1  1  0  0   3
    Ivory Coast                1  1  0  0   3
    Curaçao                    1  0  0  1   0
    Ecuador                    1  0  0  1   0
    
    GROUP F
    Team                      MP  W  D  L Pts
    Sweden                     1  1  0  0   3
    Netherlands                1  0  1  0   1
    Japan                      1  0  1  0   1
    Tunisia                    1  0  0  1   0
    
    GROUP H
    Team                      MP  W  D  L Pts
    Spain                      1  0  1  0   1
    Cape Verde                 1  0  1  0   1
    Saudi Arabia               0  0  0  0   0
    Uruguay                    0  0  0  0   0
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
