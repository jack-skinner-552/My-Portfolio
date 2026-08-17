// Main.java
import api.FootballApiClient;
import model.Match;
import model.Stadium;
import model.Group;
import model.GroupTeam;
import model.Team;
import model.GamesResponse;
import model.GroupsResponse;
import model.TeamsResponse;
import model.TeamStanding;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

public class Main {

    public static void main(String[] args) {

        try {
            FootballApiClient client = new FootballApiClient();

            GamesResponse gamesResponse = null;
            GroupsResponse groupsResponse = null;
            TeamsResponse teamsResponse = null;

            boolean flagEmojisOn = false;

            try {
                gamesResponse = client.getGames();
            } catch (Exception e) {
                System.out.println("ERR: Unable to retrieve games.");
            }

            try {
                groupsResponse = client.getGroups();
            } catch (Exception e) {
                System.out.println("ERR: Unable to retrieve groups.");
            }

            try {
                teamsResponse = client.getTeams();
            } catch (Exception e) {
                System.out.println("ERR: Unable to retrieve teams.");
            }

            StringBuilder report = new StringBuilder();

            Map<String, TeamInfo> teamRegistry = new HashMap<>();

            if (teamsResponse != null && gamesResponse != null && groupsResponse != null) {

                for (Team t : teamsResponse.getTeams()) {
                    TeamInfo info = new TeamInfo();
                    info.id = t.getId();
                    info.name = t.getNameEn();
                    info.iso2 = t.getIso2();
                    info.flag = flagEmojisOn ? countryCodeToEmoji(t.getIso2()) : "";

                    teamRegistry.put(info.id, info);
                }

                List<Match> games = gamesResponse.getGames();
                List<Group> groups = groupsResponse.getGroups();

                // STEP 1: build standings from games (single source of truth)
                Map<String, TeamStanding> standings =
                        buildStandingsFromGames(games, teamRegistry);

                // STEP 2: build everything from standings
                buildGames(report, games, teamRegistry);
                buildGroups(report, groups, teamRegistry, standings);
                buildRanks(report, groups, teamRegistry, standings);
            }

            if (gamesResponse == null &&
                    groupsResponse == null &&
                    teamsResponse == null) {

                System.out.println("ERR: Unable to retrieve data from World Cup API.\n");
            }


            String output = report.toString();

            // Console output

            System.out.print(output);

            // Save to file

            saveReport(output);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }



    private static String safeScore(int score) {
        return String.valueOf(score);
    }

    private static final DateTimeFormatter API_FORMAT =
            DateTimeFormatter.ofPattern("MM/dd/yyyy HH:mm");

    private static final DateTimeFormatter DISPLAY_FORMAT =
            DateTimeFormatter.ofPattern("MM dd, yyyy h:mm a z");

    static class TeamInfo {
        String id;
        String name;
        String iso2;
        String flag;
    }

    private static String name(Map<String, TeamInfo> reg, String id) {
        TeamInfo t = reg.get(id);
        return t != null ? t.name : "Unknown";
    }

    private static String flag(Map<String, TeamInfo> reg, String id) {
        TeamInfo t = reg.get(id);
        return t != null ? t.flag : "";
    }

    private static LocalDate extractMatchDate(Match match) {
        try {
            LocalDateTime dateTime =
                    LocalDateTime.parse(match.getLocalDate(), API_FORMAT);
            return dateTime.toLocalDate();
        } catch (Exception e) {
            System.out.println("Failed to parse date: " + match.getLocalDate());
            return null;
        }
    }

    private static String getLocalKickoffTime(
            String apiDate,
            ZoneId stadiumZone) {

        try {
            LocalDateTime matchTime =
                    LocalDateTime.parse(apiDate, API_FORMAT);

            ZonedDateTime stadiumTime =
                    matchTime.atZone(stadiumZone);

            ZonedDateTime userTime =
                    stadiumTime.withZoneSameInstant(ZoneId.systemDefault());

            return userTime.format(DISPLAY_FORMAT);

        } catch (Exception e) {
            return apiDate;
        }
    }

    private static String formatScorers(String scorers) {
        if (scorers == null ||
                scorers.equals("null") ||
                scorers.isBlank()) {
            return null;
        }

        return scorers
                .replace("{", "")
                .replace("}", "")
                .replace("\"", "");
    }
    private static String countryCodeToEmoji(String countryCode) {

        if (countryCode == null || countryCode.length() != 2) {
            return "";
        }

        countryCode = countryCode.toUpperCase();

        int firstLetter = Character.codePointAt(countryCode, 0) - 'A' + 0x1F1E6;
        int secondLetter = Character.codePointAt(countryCode, 1) - 'A' + 0x1F1E6;

        return new String(Character.toChars(firstLetter))
                + new String(Character.toChars(secondLetter));
    }

    private static boolean groupHasResults(Group group) {
        return group.getTeams().stream().anyMatch(team ->
                                !team.getMp().equals("0") ||
                                !team.getW().equals("0") ||
                                !team.getD().equals("0") ||
                                !team.getL().equals("0") ||
                                !team.getPts().equals("0")
                );
    }
    private static Map<String, TeamStanding> buildStandingsFromGames(
            List<Match> games,
            Map<String, TeamInfo> teamRegistry
    ) {
        Map<String, TeamStanding> table = new HashMap<>();

        for (Match match : games) {

            // only finished group matches
            if (!"TRUE".equalsIgnoreCase(match.getFinished())) continue;
            if (!"group".equalsIgnoreCase(match.getType())) continue;

            String homeId = match.getHomeTeamId();
            String awayId = match.getAwayTeamId();

            int homeScore = match.getHomeScore();
            int awayScore = match.getAwayScore();

            table.putIfAbsent(homeId, new TeamStanding());
            table.putIfAbsent(awayId, new TeamStanding());

            TeamStanding home = table.get(homeId);
            TeamStanding away = table.get(awayId);

            home.teamId = homeId;
            away.teamId = awayId;

            home.name = name(teamRegistry, homeId);
            away.name = name(teamRegistry, awayId);

            home.addMatch(homeScore, awayScore);
            away.addMatch(awayScore, homeScore);
        }

        return table;
    }

    private static void buildGames(StringBuilder report, List<Match> games, Map<String, TeamInfo> teamRegistry) {

        LocalDate today = LocalDate.now();
        ZonedDateTime now = ZonedDateTime.now();
        DateTimeFormatter dateFormat =
                DateTimeFormatter.ofPattern("MMMM dd, yyyy \nhh:mm z \n");

        report.append("\nFIFA World Cup 2026 Daily Report").append("\n");
        report.append(now.format(dateFormat) + "\n");
        report.append("=====================================\n");

        report.append("\nMATCHES TODAY\n");

        games.stream()
                // 1. Sort earliest → latest
                .sorted((m1, m2) -> {
                    LocalDateTime t1 = LocalDateTime.parse(m1.getLocalDate(), API_FORMAT);
                    LocalDateTime t2 = LocalDateTime.parse(m2.getLocalDate(), API_FORMAT);
                    return t1.compareTo(t2);
                })

                // 2. Filter ONLY today's matches
                .filter(match -> {
                    LocalDate matchDate = extractMatchDate(match);
                    return matchDate != null && matchDate.equals(today);
                })

                // 3. Print output
                .forEach(match -> {

                    Stadium stadium = Stadium.get(match.getStadiumId());

                    String homeFlag =
                            flag(teamRegistry, match.getHomeTeamId());
                    String awayFlag =
                            flag(teamRegistry, match.getAwayTeamId());

                    report.append(
                            match.getType().toUpperCase() + " MATCH\n"
                                    + homeFlag + match.getHomeTeam()
                                    + " " + safeScore(match.getHomeScore())
                                    + " - " + safeScore(match.getAwayScore())
                                    + " " + match.getAwayTeam() + awayFlag + "\n"
                    );

                    // Status
                    if ("true".equalsIgnoreCase(match.getFinished())) {
                        report.append("Status: FINISHED\n");

                    } else if ("live".equalsIgnoreCase(match.getTimeElapsed())) {
                        report.append("Status: LIVE\n");

                    } else {
                        report.append(
                                "Kickoff: " +
                                        getLocalKickoffTime(match.getLocalDate(), stadium.zoneId) + "\n"
                        );
                    }

                    report.append(stadium.name + "\n" + stadium.city + "\n");

                    // Scorers
                    String homeScorers = formatScorers(match.getHomeScorers());
                    String awayScorers = formatScorers(match.getAwayScorers());

                    if (homeScorers != null) {
                        report.append(match.getHomeTeam()).append(" Scorers:\n");

                        for (String scorer : homeScorers.split(",")) {
                            report.append("- ")
                                    .append(scorer.trim())
                                    .append("\n");
                        }
                    }

                    if (awayScorers != null) {
                        report.append(match.getAwayTeam()).append(" Scorers:\n");

                        for (String scorer : awayScorers.split(",")) {
                            report.append("- ")
                                    .append(scorer.trim());
                        }
                    }

                    report.append("\n\n-------------------------------------\n\n");
                });
    }
    private static void buildGroups(
            StringBuilder report, List<Group> groups,
            Map<String, TeamInfo> teamRegistry,
            Map<String, TeamStanding> standings) {

        report.append("\nGROUP STANDINGS (RECALCULATED)\n");
        report.append("================================\n");

        for (Group group : groups) {

            List<TeamStanding> groupTeams = group.getTeams().stream()
                    .map(t -> standings.get(t.getTeamId()))
                    .filter(Objects::nonNull)
                    .sorted(
                            Comparator.comparingInt((TeamStanding t) -> t.pts)
                                    .thenComparingInt(t -> t.gd())
                                    .thenComparingInt(t -> t.gf)
                                    .reversed()
                    )
                    .toList();

            // Hide empty groups (all 0 stats)
            if (groupTeams.stream().allMatch(t -> t.mp == 0)) continue;

            report.append("\nGROUP ").append(group.getName()).append("\n");
            report.append(
                    String.format(
                            "%-30s %2s %2s %2s %2s %3s %2s%n",
                            "Team", "MP", "W", "D", "L", "Pts", "GD"
                    )
            );

            for (TeamStanding t : groupTeams) {

                String gflag = flag(teamRegistry, t.teamId);
                String flagPrefix = gflag.isBlank() ? "" : gflag + " ";

                report.append(String.format(
                        "%-30s %2s %2s %2s %2s %3s %2s%n",
                        flagPrefix + t.name,
                        t.mp, t.w, t.d, t.l, t.pts, t.gd()
                ));
            }
        }
    }

    public record ThirdPlaceTeam(
            String teamId,
            String teamName,
            String flag,
            int points,
            int goalDifference,
            int goalsScored
    ) {}

    private record EliminatedTeam(
            String group,
            String teamName,
            String flag,
            int position,
            int points,
            int goalDifference,
            int goalsScored
    ) {}

    private static final Comparator<GroupTeam> STANDINGS_COMPARATOR =
            Comparator
                    .comparingInt((GroupTeam t) -> Integer.parseInt(t.getPts()))
                    .reversed()
                    .thenComparingInt(t -> Integer.parseInt(t.getGd()))
                    .reversed()
                    .thenComparingInt(t -> Integer.parseInt(t.getGf()))
                    .reversed();

    private static void buildRanks(
            StringBuilder report,
            List<Group> groups,
            Map<String, TeamInfo> teamRegistry,
            Map<String, TeamStanding> standings) {

        report.append("\nTEAMS ADVANCING IF THE WORLD CUP ENDED TODAY\n");
        report.append("===========================================\n");

        List<ThirdPlaceTeam> thirdPlaceTeams = new ArrayList<>();

        // STEP 2: process each group using REAL standings
        for (Group group : groups) {

            List<TeamStanding> groupTable = group.getTeams().stream()
                    .map(t -> {
                        TeamStanding s = standings.get(t.getTeamId());

                        if (s == null) {
                            TeamStanding empty = new TeamStanding();
                            empty.teamId = t.getTeamId();
                            empty.name = name(teamRegistry, t.getTeamId());
                            return empty;
                        }

                        return s;
                    })
                    .filter(s -> s.mp > 0 || s.pts > 0 || s.gf > 0 || s.ga > 0)
                    .sorted(
                            Comparator
                                    .comparingInt((TeamStanding t) -> t.pts).reversed()
                                    .thenComparingInt(t -> t.gd())
                                    .thenComparingInt(t -> t.gf)
                    )
                    .toList();

            // skip empty groups (no matches played)
            if (groupTable.isEmpty()) continue;

            report.append("\nGROUP ").append(group.getName()).append("\n");

            // TOP 2 ADVANCE
            for (int i = 0; i < Math.min(2, groupTable.size()); i++) {

                TeamStanding t = groupTable.get(i);

                String tflag = flag(teamRegistry, t.teamId);
                String prefix = tflag.isBlank() ? "" : tflag + " ";

                report.append(String.format(
                        "%d. %-25s Pts:%2d GD:%3d%n",
                        i + 1,
                        prefix + t.name,
                        t.pts,
                        t.gd()
                ));
            }

            // THIRD PLACE COLLECTION
            if (groupTable.size() >= 3) {

                TeamStanding third = groupTable.get(2);

                thirdPlaceTeams.add(new ThirdPlaceTeam(
                        third.teamId,
                        third.name,
                        flag(teamRegistry, third.teamId),
                        third.pts,
                        third.gd(),
                        third.gf
                ));
            }
        }

        // STEP 3: rank third-place teams correctly
        List<ThirdPlaceTeam> rankedThirdPlaceTeams = thirdPlaceTeams.stream()
                .sorted(
                        Comparator
                                .comparingInt(ThirdPlaceTeam::points).reversed()
                                .thenComparing(ThirdPlaceTeam::goalDifference, Comparator.reverseOrder())
                                .thenComparing(ThirdPlaceTeam::goalsScored, Comparator.reverseOrder())
                )
                .toList();

        List<ThirdPlaceTeam> bestEight = rankedThirdPlaceTeams.stream().limit(8).toList();
        List<ThirdPlaceTeam> bottomThirds = rankedThirdPlaceTeams.stream().skip(8).toList();

        report.append("\nTOP 8 THIRD-PLACE TEAMS\n");
        report.append("If the World Cup ended today, these teams would also advance.\n");
        report.append("===========================================================\n");

        int rank = 1;
        for (ThirdPlaceTeam t : bestEight) {

            String prefix = t.flag().isBlank() ? "" : t.flag() + " ";

            report.append(String.format(
                    "%d. %-25s Pts:%2d GD:%3d GF:%2d%n",
                    rank++,
                    prefix + t.teamName(),
                    t.points(),
                    t.goalDifference(),
                    t.goalsScored()
            ));
        }

        // STEP 4: eliminated teams
        List<EliminatedTeam> fourthPlaceTeams = groups.stream()

                .filter(Main::groupHasResults)
                .map(group -> {

                    List<TeamStanding> table = group.getTeams().stream()
                            .map(t -> standings.get(t.getTeamId()))
                            .filter(Objects::nonNull)
                            .sorted(
                                    Comparator
                                            .comparingInt((TeamStanding t) -> t.pts).reversed()
                                            .thenComparingInt(t -> t.gd())
                                            .thenComparingInt(t -> t.gf)
                            )
                            .toList();

                    if (table.size() < 4) return null;

                    TeamStanding fourth = table.get(3);

                    return new EliminatedTeam(
                            group.getName(),
                            fourth.name,
                            flag(teamRegistry, fourth.teamId),
                            4,
                            fourth.pts,
                            fourth.gd(),
                            fourth.gf
                    );
                })
                .filter(Objects::nonNull)
                .toList();

        report.append("\nELIMINATED IF WORLD CUP ENDED TODAY\n");
        report.append("===================================\n");

        report.append("\nBottom Third-Place Teams\n");
        report.append("------------------------\n");

        for (ThirdPlaceTeam t : bottomThirds) {

            String prefix = t.flag().isBlank() ? "" : t.flag() + " ";

            report.append(String.format(
                    "%-25s Pts:%2d GD:%3d GF:%2d%n",
                    prefix + t.teamName(),
                    t.points(),
                    t.goalDifference(),
                    t.goalsScored()
            ));
        }

        if (bottomThirds.size() < 4) {
            report.append("\nNote: Some groups have not completed matches yet.\n");
        }

        report.append("\nFourth-Place Teams\n");
        report.append("------------------\n");

        for (EliminatedTeam t : fourthPlaceTeams) {

            String prefix = t.flag().isBlank() ? "" : t.flag() + " ";

            report.append(String.format(
                    "Group %-2s %-25s Pts:%2d GD:%3d GF:%2d%n",
                    t.group(),
                    prefix + t.teamName(),
                    t.points(),
                    t.goalDifference(),
                    t.goalsScored()
            ));
        }
    }
    private static void saveReport(String report) {

        try {

            String timestamp = LocalDateTime.now()
                    .format(DateTimeFormatter.ofPattern("yyyy-MM-dd_HH-mm"));

            String fileName =
                    "WorldCupReport_" +
                            timestamp +
                            ".txt";

            Path path = Paths.get(fileName);

            Files.writeString(path, report, StandardCharsets.UTF_8);

            System.out.println(
                    "\nReport saved to: " +
                            path.toAbsolutePath());

        } catch (Exception e) {

            System.out.println(
                    "Failed to save report file.");

            e.printStackTrace();
        }
    }



}