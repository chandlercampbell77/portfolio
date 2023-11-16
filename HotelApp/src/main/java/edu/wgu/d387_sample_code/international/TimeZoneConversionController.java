package edu.wgu.d387_sample_code.international;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.time.ZonedDateTime;

@RestController
public class TimeZoneConversionController {

    @GetMapping("/api/convert-time")
    public String getConvertedTime() {
        TimeConversion converter = new TimeConversion();

        ZonedDateTime presentationTime = ZonedDateTime.now();

        return converter.convertTimeZones(presentationTime);
    }
}
