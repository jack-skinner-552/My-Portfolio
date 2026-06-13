// Match.java
package model;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Match {

    @JsonProperty("_id")
    private String mongoId;

    @JsonProperty("id")
    private String id;

    private String group;

    @JsonProperty("home_team_name_en")
    private String homeTeam;

    @JsonProperty("away_team_name_en")
    private String awayTeam;

    @JsonProperty("home_score")
    private int homeScore;

    @JsonProperty("away_score")
    private int awayScore;

    @JsonProperty("local_date")
    private String localDate;

    private String finished;

    @JsonProperty("time_elapsed")
    private String timeElapsed;

    @JsonProperty("home_scorers")
    private String homeScorers;

    @JsonProperty("away_scorers")
    private String awayScorers;

    @JsonProperty("stadium_id")
    private String stadiumId;

    public Match() {
    }

    public String getId() {
        return id != null ? id : mongoId;
    }

    public String getGroup() {
        return group;
    }

    public String getHomeTeam() {
        return homeTeam;
    }

    public String getAwayTeam() {
        return awayTeam;
    }

    public int getHomeScore() {
        return homeScore;
    }

    public int getAwayScore() {
        return awayScore;
    }

    public String getLocalDate() {
        return localDate;
    }

    public String getFinished() {
        return finished;
    }

    public String getTimeElapsed() {
        return timeElapsed;
    }

    public String getHomeScorers() {
        return homeScorers;
    }

    public String getAwayScorers() {
        return awayScorers;
    }

    public String getStadiumId() { return stadiumId;}
}