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

public class FootballApiClient {

    private static final String GAMES_URL =
            "https://worldcup26.ir/get/games";

    private static final String GROUPS_URL =
            "https://worldcup26.ir/get/groups";

    private static final String TEAMS_URL =
            "https://worldcup26.ir/get/teams";

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    public FootballApiClient() {
        this.httpClient = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .build();
        this.objectMapper = new ObjectMapper();
    }

    public GamesResponse getGames()
            throws IOException, InterruptedException {

        int maxRetries = 3;

        for (int attempt = 1; attempt <= maxRetries; attempt++) {

            try {

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(GAMES_URL))
                        .GET()
                        .build();

                HttpResponse<String> response =
                        httpClient.send(
                                request,
                                HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 500) {

                    System.out.printf(
                            "Server returned HTTP 500 (attempt %d/%d)%n",
                            attempt,
                            maxRetries);

                    if (attempt == maxRetries) {
                        throw new RuntimeException(
                                "Server returned HTTP 500 after "
                                        + maxRetries
                                        + " attempts.");
                    }

                    Thread.sleep(2000);
                    continue;
                }

                if (response.statusCode() != 200) {
                    throw new RuntimeException(
                            "HTTP Error: " + response.statusCode());
                }

                return objectMapper.readValue(
                        response.body(),
                        GamesResponse.class);

            } catch (javax.net.ssl.SSLHandshakeException e) {

                System.out.printf(
                        "SSL handshake failed retrieving games (attempt %d/%d)%n",
                        attempt,
                        maxRetries);

                if (attempt == maxRetries) {
                    throw e;
                }

                Thread.sleep(2000);
            }
        }

        throw new RuntimeException("Failed to retrieve games.");
    }

    public GroupsResponse getGroups()
            throws IOException, InterruptedException {

        int maxRetries = 3;

        for (int attempt = 1; attempt <= maxRetries; attempt++) {

            try {

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(GROUPS_URL))
                        .GET()
                        .build();

                HttpResponse<String> response =
                        httpClient.send(
                                request,
                                HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 500) {

                    System.out.printf(
                            "Server returned HTTP 500 (attempt %d/%d)%n",
                            attempt,
                            maxRetries);

                    if (attempt == maxRetries) {
                        throw new RuntimeException(
                                "Server returned HTTP 500 after "
                                        + maxRetries
                                        + " attempts.");
                    }

                    Thread.sleep(2000);
                    continue;
                }

                if (response.statusCode() != 200) {
                    throw new RuntimeException(
                            "HTTP Error: " + response.statusCode());
                }

                return objectMapper.readValue(
                        response.body(),
                        GroupsResponse.class);

            } catch (javax.net.ssl.SSLHandshakeException e) {

                System.out.printf(
                        "SSL handshake failed retrieving groups (attempt %d/%d)%n",
                        attempt,
                        maxRetries);

                if (attempt == maxRetries) {
                    throw e;
                }

                Thread.sleep(2000);
            }
        }

        throw new RuntimeException("Failed to retrieve groups.");
    }

    public TeamsResponse getTeams()
            throws IOException, InterruptedException {

        int maxRetries = 3;

        for (int attempt = 1; attempt <= maxRetries; attempt++) {

            try {

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(TEAMS_URL))
                        .GET()
                        .build();

                HttpResponse<String> response =
                        httpClient.send(
                                request,
                                HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 500) {

                    System.out.printf(
                            "Server returned HTTP 500 (attempt %d/%d)%n",
                            attempt,
                            maxRetries);

                    if (attempt == maxRetries) {
                        throw new RuntimeException(
                                "Server returned HTTP 500 after "
                                        + maxRetries
                                        + " attempts.");
                    }

                    Thread.sleep(2000);
                    continue;
                }

                if (response.statusCode() != 200) {
                    throw new RuntimeException(
                            "HTTP Error: " + response.statusCode());
                }

                return objectMapper.readValue(
                        response.body(),
                        TeamsResponse.class);

            } catch (javax.net.ssl.SSLHandshakeException e) {

                System.out.printf(
                        "SSL handshake failed retrieving teams (attempt %d/%d)%n",
                        attempt,
                        maxRetries);

                if (attempt == maxRetries) {
                    throw e;
                }

                Thread.sleep(2000);
            }
        }

        throw new RuntimeException("Failed to retrieve teams.");
    }
}