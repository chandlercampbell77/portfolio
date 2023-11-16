package edu.wgu.d387_sample_code.international;

import org.springframework.context.MessageSource;
import org.springframework.stereotype.Service;

import java.util.Locale;

@Service
public class DisplayMessage {

    private final MessageSource messageSource;

    public DisplayMessage(MessageSource messageSource) {
        this.messageSource = messageSource;
    }

    public String getWelcomeMessage(Locale locale) {
        return messageSource.getMessage("welcomeMessage", null, locale);
    }

}
