package edu.wgu.d387_sample_code.international;
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class TimeConversion {

    public String convertTimeZones(ZonedDateTime inputTime) {
        ZoneId etZone = ZoneId.of("America/New_York");
        ZoneId mtZone = ZoneId.of("America/Denver");
        ZoneId utcZone = ZoneId.of("UTC");

        ZonedDateTime etTime = inputTime.withZoneSameInstant(etZone);
        ZonedDateTime mtTime = inputTime.withZoneSameInstant(mtZone);
        ZonedDateTime utcTime = inputTime.withZoneSameInstant(utcZone);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");

        String convertedTimes = String.format("ET: %s, MT: %s, UTC: %s",
                etTime.format(formatter),
                mtTime.format(formatter),
                utcTime.format(formatter));

        return convertedTimes;
    }
}
