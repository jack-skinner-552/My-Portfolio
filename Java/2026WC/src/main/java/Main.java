// Main.java
import api.FootballApiClient;
import model.Match;
import model.Stadium;
import model.Group;
import model.Team;
import model.GamesResponse;
import model.GroupsResponse;
import model.TeamsResponse;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Objects;
import java.util.Map;
import java.util.stream.Collectors;

public class Main {

    public static void main(String[] args) {

        try {
            FootballApiClient client = new FootballApiClient();

            GamesResponse gamesResponse = null;
            GroupsResponse groupsResponse = null;
            TeamsResponse teamsResponse = null;

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

            if (gamesResponse != null) {
                List<Match> games = gamesResponse.getGames();
                buildGames(report, games);
            }

            if (groupsResponse != null && teamsResponse != null) {

                List<Group> groups = groupsResponse.getGroups();
                List<Team> teams = teamsResponse.getTeams();

                Map<String, String> teamMap = teams.stream()
                        .collect(Collectors.toMap(
                                Team::getId,
                                Team::getNameEn
                        ));

                buildGroups(report, groups, teamMap);
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
            DateTimeFormatter.ofPattern("MM dd, yyy h:mm a z");

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

    private static void buildGames(StringBuilder report, List<Match> games) {

        LocalDate today = LocalDate.now();
        ZonedDateTime now = ZonedDateTime.now();
        DateTimeFormatter dateFormat =
                DateTimeFormatter.ofPattern("MMMM dd, yyyy \nhh:mm z \n");

        report.append("\nFIFA World Cup 2026 Daily Report").append("\n");
        report.append(now.format(dateFormat) + "\n");
        report.append("=====================================\n");

        report.append("MATCHES TODAY\n");

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

                    report.append(
                            match.getHomeTeam()
                                    + " " + safeScore(match.getHomeScore())
                                    + " - " + safeScore(match.getAwayScore())
                                    + " " + match.getAwayTeam() + "\n"
                    );

                    // Status
                    if ("true".equalsIgnoreCase(match.getFinished())) {
                        report.append("Status: FINISHED\n");

                    } else if (match.getHomeScore() > 0
                            || match.getAwayScore() > 0
                            || match.getTimeElapsed().equals("live")) {
                        report.append("Status: LIVE\n");

                    } else {
                        report.append(
                                "Kickoff: " +
                                        getLocalKickoffTime(match.getLocalDate(), stadium.zoneId) + "\n"
                        );
                    }

                    report.append(stadium.name + "\n" + stadium.city);

                    // Scorers
                    if (!Objects.equals(match.getHomeScorers(), "null")) {
                        report.append("\n" + match.getHomeTeam() + " Scorers:\n");
                        report.append("- " + match.getHomeScorers() + "\n");

                        if (!Objects.equals(match.getAwayScorers(), "null")) {
                            report.append("\n" + match.getAwayTeam() + " Scorers:\n");
                            report.append("- " + match.getAwayScorers() + "\n");
                        }
                    }

                    report.append("\n-------------------------------------\n");
                });
    }
    private static void buildGroups(StringBuilder report, List<Group> groups, Map<String, String> teamMap) {

        report.append("\nGROUP STANDINGS\n");
        report.append("==============================\n");

        groups.stream()

                // Sort groups A → L
                .sorted((g1, g2) -> g1.getName().compareTo(g2.getName()))

                // Hide empty groups (all stats = 0)
                .filter(group -> group.getTeams().stream().anyMatch(team ->
                        !team.getMp().equals("0") ||
                                !team.getW().equals("0") ||
                                !team.getD().equals("0") ||
                                !team.getL().equals("0") ||
                                !team.getPts().equals("0")
                ))

                .forEach(group -> {

                    report.append("\nGROUP " + group.getName() + "\n");

                    report.append(
                            String.format(
                                    "%-25s %2s %2s %2s %2s %3s%n",
                                    "Team", "MP", "W", "D", "L", "Pts"
                            )
                    );

                    group.getTeams().stream()

                            // Sort by points (desc)
                            .sorted((a, b) ->
                                    Integer.compare(
                                            Integer.parseInt(b.getPts()),
                                            Integer.parseInt(a.getPts())
                                    )
                            )

                            .forEach(team -> {

                                String id = team.getTeamId();

                                if (id != null) {
                                    id = id.trim();
                                }

                                String teamName = teamMap.getOrDefault(id, "Unknown Team");

                                report.append(
                                        String.format(
                                                "%-25s %2s %2s %2s %2s %3s%n",
                                                teamName,
                                                team.getMp(),
                                                team.getW(),
                                                team.getD(),
                                                team.getL(),
                                                team.getPts()
                                        )
                                );
                            });
                });

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

            Files.writeString(path, report);

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