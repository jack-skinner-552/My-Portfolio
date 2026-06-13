// Main.java
import api.FootballApiClient;
import model.Match;
import model.Stadium;

import java.time.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Objects;

public class Main {

    public static void main(String[] args) {

        try {
            FootballApiClient client = new FootballApiClient();
            var response = client.getGames();

            List<Match> games = response.getGames();

            printReport(games);

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
        DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("MMMM dd, yyyy");

        System.out.println("FIFA World Cup 2026 Daily Report");
        System.out.println(today.format(dateFormat));
        System.out.println("=====================================\n");

        System.out.println("MATCHES TODAY\n");

        for (Match match : games) {

            Stadium stadium = Stadium.get(match.getStadiumId());
            LocalDate matchDate = extractMatchDate(match);

            // 🚨 ONLY TODAY
            if (matchDate == null || !matchDate.equals(today)) {
                continue;
            }

            System.out.println(match.getHomeTeam() +
                    " " + safeScore(match.getHomeScore()) +
                    " - " + safeScore(match.getAwayScore()) +
                    " " + match.getAwayTeam());

            if ("true".equalsIgnoreCase(match.getFinished())) {
                System.out.println("Status: FINISHED");
            } else if (match.getHomeScore() > 0 || match.getAwayScore() > 0) {
                System.out.println("Status: LIVE");
            } else {
                System.out.println("Kickoff: " + getLocalKickoffTime(match.getLocalDate(), stadium.zoneId));
            }
            System.out.println(stadium.name + "\n" + stadium.city);

            if (!Objects.equals(match.getHomeScorers(), "null")) {
                System.out.println("\n"+ match.getHomeTeam() +" Scorers:");
                System.out.println("- " + match.getHomeScorers());

                if (!Objects.equals(match.getAwayScorers(), "null")) {
                    System.out.println("\n"+ match.getAwayTeam() +" Scorers:");
                    System.out.println("- " + match.getAwayScorers());
                }
            }

            System.out.println("\n-------------------------------------\n");
        }
    }



}