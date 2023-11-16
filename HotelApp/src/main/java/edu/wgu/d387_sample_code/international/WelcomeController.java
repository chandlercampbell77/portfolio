package edu.wgu.d387_sample_code.international;
import org.springframework.web.bind.annotation.*;
import java.util.concurrent.Callable;
import java.util.*;

@RestController
@CrossOrigin
@RequestMapping("/api")
public class WelcomeController {

    private final DisplayMessage displayMessage;

    public WelcomeController(DisplayMessage displayMessage) {
        this.displayMessage = displayMessage;
    }

    @GetMapping("/welcome-messages")
    public List<String> getWelcomeMessages() throws InterruptedException {
        List<String> messages = new ArrayList<>();

        Thread englishThread = new Thread(() -> {
            String message = displayMessage.getWelcomeMessage(new Locale("en", "US"));
            synchronized (messages) {
                messages.add(message);
            }
        });

        Thread frenchThread = new Thread(() -> {
            String message = displayMessage.getWelcomeMessage(new Locale("fr", "CA"));
            synchronized (messages) {
                messages.add(message);
            }
        });

        englishThread.start();
        frenchThread.start();

        englishThread.join();
        frenchThread.join();

        return messages;
    }
}
