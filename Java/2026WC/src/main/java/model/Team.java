package model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Team {

    @JsonProperty("id")
    private String id;          // <-- THIS is the GROUP reference ID (1–48)

    @JsonProperty("iso2")
    private String iso2;

    @JsonProperty("name_en")
    private String nameEn;

    public String getId() {
        return id;
    }

    public String getIso2() {
        return iso2;
    }

    public String getNameEn() {
        return nameEn;
    }
}