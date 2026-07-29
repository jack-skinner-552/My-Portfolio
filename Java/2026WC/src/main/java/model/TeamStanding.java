package model;

public class TeamStanding {
    public String teamId;
    public String name;
    public int mp;
    public int w;
    public int d;
    public int l;
    public int gf;
    public int ga;

    public int pts;

    public void addMatch(int scored, int conceded) {
        mp++;
        gf += scored;
        ga += conceded;

        if (scored > conceded) {
            w++;
            pts += 3;
        } else if (scored < conceded) {
            l++;
        } else {
            d++;
            pts += 1;
        }
    }

    public int gd() {
        return gf - ga;
    }

}