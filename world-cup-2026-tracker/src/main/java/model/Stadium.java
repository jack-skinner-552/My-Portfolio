package model;

import java.time.ZoneId;
import java.util.Map;

public class Stadium {

    public final String id;
    public final String name;
    public final String city;
    public final ZoneId zoneId;

    public Stadium(String id, String name, String city, ZoneId zoneId) {
        this.id = id;
        this.name = name;
        this.city = city;
        this.zoneId = zoneId;
    }

    // --- Static registry of all stadiums ---
    private static final Map<String, Stadium> STADIUMS =
            Map.ofEntries(
                    Map.entry("1", new Stadium("1", "Estadio Azteca", "Mexico City, MEX", ZoneId.of("America/Mexico_City"))),
                    Map.entry("2", new Stadium("2", "Estadio Akron", "Guadalajara, MEX", ZoneId.of("America/Mexico_City"))),
                    Map.entry("3", new Stadium("3", "Estadio BBVA", "Monterrey, MEX", ZoneId.of("America/Monterrey"))),

                    Map.entry("4", new Stadium("4", "AT&T Stadium", "Arlington, TX", ZoneId.of("America/Chicago"))),
                    Map.entry("5", new Stadium("5", "NRG Stadium", "Houston, TX", ZoneId.of("America/Chicago"))),
                    Map.entry("6", new Stadium("6", "Arrowhead Stadium", "Kansas City, MS", ZoneId.of("America/Chicago"))),

                    Map.entry("7", new Stadium("7", "Mercedes-Benz Stadium", "Atlanta, GA", ZoneId.of("America/New_York"))),
                    Map.entry("8", new Stadium("8", "Hard Rock Stadium", "Miami, FL", ZoneId.of("America/New_York"))),
                    Map.entry("9", new Stadium("9", "Gillette Stadium", "Foxborough, MA", ZoneId.of("America/New_York"))),
                    Map.entry("10", new Stadium("10", "Lincoln Financial Field", "Philadelphia, PN", ZoneId.of("America/New_York"))),
                    Map.entry("11", new Stadium("11", "MetLife Stadium", "East Rutherford, NJ", ZoneId.of("America/New_York"))),

                    Map.entry("12", new Stadium("12", "BMO Field", "Toronto, CAN", ZoneId.of("America/Toronto"))),
                    Map.entry("13", new Stadium("13", "BC Place", "Vancouver, CAN", ZoneId.of("America/Vancouver"))),

                    Map.entry("14", new Stadium("14", "Lumen Field", "Seattle, WA", ZoneId.of("America/Los_Angeles"))),
                    Map.entry("15", new Stadium("15", "Levi's Stadium", "Santa Clara, CA", ZoneId.of("America/Los_Angeles"))),
                    Map.entry("16", new Stadium("16", "SoFi Stadium", "Los Angeles, CA", ZoneId.of("America/Los_Angeles")))
            );

    public static Stadium get(String id) {
        return STADIUMS.get(id);
    }
}