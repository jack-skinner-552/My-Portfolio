// FootballApiClient.java
package api;

import com.fasterxml.jackson.databind.ObjectMapper;
import model.GamesResponse;
import model.GroupsResponse;
import model.TeamsResponse;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import javax.net.ssl.SSLHandshakeException;

public class FootballApiClient {

    private static final String GAMES_URL =
            "https://worldcup26.ir/get/games";

    private static final String GROUPS_URL =
            "https://worldcup26.ir/get/groups";

    private static final String TEAMS_URL =
            "https://worldcup26.ir/get/teams";

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    private static final int TOTAL_REQUESTS = 3;
    private static int completedRequests = 0;

    public FootballApiClient() {
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .build();
        this.objectMapper = new ObjectMapper();
    }

    public GamesResponse getGames()
            throws IOException, InterruptedException {

        String json =
                getWithRetry(GAMES_URL, "Games");

        updateProgressBar("Games Retrieved.");
        return objectMapper.readValue(
                json,
                GamesResponse.class);
    }

    public GroupsResponse getGroups()
            throws IOException, InterruptedException {

        String json =
                getWithRetry(GROUPS_URL, "Groups");

        updateProgressBar("Groups Retrieved.");
        return objectMapper.readValue(
                json,
                GroupsResponse.class);
    }

    public TeamsResponse getTeams()
            throws IOException, InterruptedException {

        String json =
                getWithRetry(TEAMS_URL, "Teams");

        updateProgressBar("Teams Retrieved.");
        return objectMapper.readValue(
                json,
                TeamsResponse.class);
    }

    private String getWithRetry(String url, String resourceName)
            throws IOException, InterruptedException {

        int maxRetries = 3;

        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            long waitTime = 2000L * attempt;

            try {

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .GET()
                        .build();

                HttpResponse<String> response =
                        httpClient.send(
                                request,
                                HttpResponse.BodyHandlers.ofString());

                // Retry HTTP 500
                if (response.statusCode() == 500) {

                    System.out.printf(
                            "%s returned HTTP 500 (attempt %d/%d)%n",
                            resourceName,
                            attempt,
                            maxRetries);

                    if (attempt == maxRetries) {
                        throw new RuntimeException(
                                resourceName +
                                        " returned HTTP 500 after "
                                        + maxRetries +
                                        " attempts.");
                    }

                    Thread.sleep(waitTime);
                    continue;
                }

                // Other HTTP errors
                if (response.statusCode() != 200) {
                    throw new RuntimeException(
                            "HTTP Error: " + response.statusCode());
                }

                System.out.println(
                        "Successfully Retrieved "
                                + resourceName + ".");

                return response.body();

            } catch (SSLHandshakeException e) {

                System.out.printf(
                        "SSL handshake failed retrieving %s (attempt %d/%d)%n",
                        resourceName,
                        attempt,
                        maxRetries);

                if (attempt == maxRetries) {
                    throw e;
                }

                Thread.sleep(waitTime);

            }
            catch (java.io.IOException e) {

                System.out.printf(
                        "Network error retrieving %s (attempt %d/%d): %s%n",
                        resourceName,
                        attempt,
                        maxRetries,
                        e.getMessage());

                if (attempt == maxRetries) {
                    throw e;
                }

                Thread.sleep(waitTime);
            }
        }

        throw new RuntimeException(
                "Failed to retrieve " + resourceName + ".");
    }

    private static void updateProgressBar(String label) {

        completedRequests++;

        int percent =
                (completedRequests * 100) / TOTAL_REQUESTS;

        int barLength = 20;

        int filled =
                (completedRequests * barLength) / TOTAL_REQUESTS;

        StringBuilder bar = new StringBuilder();

        bar.append("[");

        for (int i = 0; i < barLength; i++) {
            if (i < filled) {
                bar.append("█");
            } else {
                bar.append("-");
            }
        }

        bar.append("]");

        System.out.printf(
                "%s %3d%% - %s%n",
                bar,
                percent,
                label
        );
    }
}