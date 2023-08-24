import java.util.ArrayList;
import java.util.List;

public class EmergencyAlertSystem {

    // Function to capture images using the Raspberry Pi Camera module
    public static boolean captureImages() {
        // Simulate capturing images (replace with actual camera code)
        System.out.println("Capturing images...");
        try {
            Thread.sleep(2000); // Simulate image capture time
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return true; // Return true if successful, false otherwise
    }

    // Function to send an email with captured images
    public static boolean sendEmail(String recipient, String subject, String body, List<String> imagePaths) {
        // Simulate sending email (replace with actual email code)
        System.out.println("Sending email to: " + recipient);
        System.out.println("Subject: " + subject);
        System.out.println("Body: " + body);

        System.out.print("Attached Images: ");
        for (String imagePath : imagePaths) {
            System.out.print(imagePath + ", ");
        }
        System.out.println();

        return true; // Return true if email sent successfully, false otherwise
    }

    public static void main(String[] args) {
        // Simulate button press to activate the device
        System.out.println("Press the emergency button to activate the safety device...");
        try {
            Thread.sleep(2000); // Simulate button press
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Capture images
        if (captureImages()) {
            // Images captured successfully

            // GPS coordinates
            double latitude = 18.463620852371374;
            double longitude = 73.86815756783137;

            // Compose email subject and body
            String subject = "Emergency Alert!";
            String body = "This is an emergency alert. Please respond immediately.";

            // Attach captured images
            List<String> imagePaths = new ArrayList<>();
            imagePaths.add("image1.jpg");
            imagePaths.add("image2.jpg");
            imagePaths.add("image3.jpg");

            // Send email to the nearest police station
            String recipient = "police@example.com";
            if (sendEmail(recipient, subject, body, imagePaths)) {
                System.out.println("Emergency alert email sent successfully!");
            } else {
                System.out.println("Failed to send the emergency alert email.");
            }
        } else {
            System.out.println("Failed to capture images. Check the camera module.");
        }
    }
}
