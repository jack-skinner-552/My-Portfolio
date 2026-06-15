// TeamsResponse.java
package model;

import java.util.List;

public class TeamsResponse {

    private List<Team> teams;

    public TeamsResponse() {}

    public List<Team> getTeams() {
        return teams;
    }

    public void setTeams(List<Team> teams) {
        this.teams = teams;
    }
}