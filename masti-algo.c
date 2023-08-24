#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>

// Function to capture images using the Raspberry Pi Camera module
bool captureImages() {
    // Simulate capturing images (replace with actual camera code)
    printf("Capturing images...\n");
    sleep(2); // Simulate image capture time
    return true; // Return true if successful, false otherwise
}

// Function to send an email with captured images
bool sendEmail(const char *recipient, const char *subject, const char *body, char **imagePaths, int numImages) {
    // Simulate sending email (replace with actual email code)
    printf("Sending email to: %s\n", recipient);
    printf("Subject: %s\n", subject);
    printf("Body: %s\n", body);

    printf("Attached Images: ");
    for (int i = 0; i < numImages; i++) {
        printf("%s, ", imagePaths[i]);
    }
    printf("\n");

    return true; // Return true if email sent successfully, false otherwise
}

int main() {
    // Simulate button press to activate the device
    printf("Press the emergency button to activate the safety device...\n");
    sleep(2); // Simulate button press

    // Capture images
    if (captureImages()) {
        // Images captured successfully

        // GPS coordinates
        double latitude = 18.4636;
        double longitude = 73.8681;

        // Compose email subject and body
        const char *subject = "Emergency Alert!";
        const char *body = "This is an emergency alert. Please respond immediately.";

        // Attach captured images
        char *imagePaths[] = {"image1.jpg", "image2.jpg", "image3.jpg"};
        int numImages = sizeof(imagePaths) / sizeof(imagePaths[0]);

        // Send email to the nearest police station
        const char *recipient = "police@example.com";
        if (sendEmail(recipient, subject, body, imagePaths, numImages)) {
            printf("Emergency alert email sent successfully!\n");
        } else {
            printf("Failed to send the emergency alert email.\n");
        }
    } else {
        printf("Failed to capture images. Check the camera module.\n");
    }

    return 0;
}
