// Main.java
import api.FootballApiClient;
import model.Match;
import model.Stadium;
import model.Group;
import model.Team;
import model.GamesResponse;
import model.GroupsResponse;
import model.TeamsResponse;

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
            GamesResponse gamesResponse = client.getGames();
            GroupsResponse groupsResponse = client.getGroups();
            TeamsResponse teamsResponse = client.getTeams();

            List<Match> games = gamesResponse.getGames();
            List<Group> groups = groupsResponse.getGroups();
            List<Team> teams = teamsResponse.getTeams();

            Map<String, String> teamMap = teams.stream()
                    .collect(Collectors.toMap(
                            Team::getId,
                            Team::getNameEn
                    ));

            printReport(games);
            printGroups(groups, teamMap);

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

    private static void printReport(List<Match> games) {

        LocalDate today = LocalDate.now();
        ZonedDateTime now = ZonedDateTime.now();
        DateTimeFormatter dateFormat =
                DateTimeFormatter.ofPattern("MMMM dd, yyyy \nhh:mm z");

        System.out.println("FIFA World Cup 2026 Daily Report");
        System.out.println(now.format(dateFormat));
        System.out.println("=====================================\n");

        System.out.println("MATCHES TODAY\n");

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

                    System.out.println(
                            match.getHomeTeam()
                                    + " " + safeScore(match.getHomeScore())
                                    + " - " + safeScore(match.getAwayScore())
                                    + " " + match.getAwayTeam()
                    );

                    // Status
                    if ("true".equalsIgnoreCase(match.getFinished())) {
                        System.out.println("Status: FINISHED");

                    } else if (match.getHomeScore() > 0
                            || match.getAwayScore() > 0
                            || match.getTimeElapsed().equals("live")) {
                        System.out.println("Status: LIVE");

                    } else {
                        System.out.println(
                                "Kickoff: " +
                                        getLocalKickoffTime(match.getLocalDate(), stadium.zoneId)
                        );
                    }

                    System.out.println(stadium.name + "\n" + stadium.city);

                    // Scorers
                    if (!Objects.equals(match.getHomeScorers(), "null")) {
                        System.out.println("\n" + match.getHomeTeam() + " Scorers:");
                        System.out.println("- " + match.getHomeScorers());

                        if (!Objects.equals(match.getAwayScorers(), "null")) {
                            System.out.println("\n" + match.getAwayTeam() + " Scorers:");
                            System.out.println("- " + match.getAwayScorers());
                        }
                    }

                    System.out.println("\n-------------------------------------\n");
                });
    }
    private static void printGroups(List<Group> groups, Map<String, String> teamMap) {

        System.out.println("\nGROUP STANDINGS");
        System.out.println("==============================");

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

                    System.out.println("\nGROUP " + group.getName());

                    System.out.printf(
                            "%-25s %2s %2s %2s %2s %3s%n",
                            "Team", "MP", "W", "D", "L", "Pts"
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

                                System.out.printf(
                                        "%-25s %2s %2s %2s %2s %3s%n",
                                        teamName,
                                        team.getMp(),
                                        team.getW(),
                                        team.getD(),
                                        team.getL(),
                                        team.getPts()
                                );
                            });
                });
    }



}