// FootballApiClient.java
package api;

import com.fasterxml.jackson.databind.ObjectMapper;
import model.GamesResponse;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class FootballApiClient {

    private static final String GAMES_URL =
            "https://worldcup26.ir/get/games";

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    public FootballApiClient() {
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    public GamesResponse getGames()
            throws IOException, InterruptedException {

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(GAMES_URL))
                .GET()
                .build();

        HttpResponse<String> response =
                httpClient.send(
                        request,
                        HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200) {
            throw new RuntimeException(
                    "HTTP Error: " + response.statusCode());
        }

        return objectMapper.readValue(
                response.body(),
                GamesResponse.class);
    }
}