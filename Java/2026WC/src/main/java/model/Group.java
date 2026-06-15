package model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import java.util.List;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Group {

    private String name;
    private List<GroupTeam> teams;

    public String getName() {
        return name;
    }

    public List<GroupTeam> getTeams() {
        return teams;
    }
}