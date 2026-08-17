package model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GroupTeam {

    @JsonProperty("team_id")
    private String teamId;

    private String mp;
    private String w;
    private String d;
    private String l;
    private String pts;
    private String gf;
    private String ga;
    private String gd;

    public String getTeamId() {
        return teamId;
    }

    public String getMp() { return mp; }
    public String getW() { return w; }
    public String getD() { return d; }
    public String getL() { return l; }
    public String getPts() { return pts; }
    public String getGf() { return gf; }
    public String getGa() { return ga; }
    public String getGd() { return gd; }
}