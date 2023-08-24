import time
import smtplib
import picamera
import RPi.GPIO as GPIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from gps import gps
import os

# Initialize GPIO pins
BUTTON_PIN = 18
BUZZER_PIN = 22
LED_PINS = [23, 24, 25]  # Replace with actual GPIO pins for LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer = GPIO.PWM(BUZZER_PIN, 1000)  # Buzzer PWM frequency
for led_pin in LED_PINS:
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.LOW)

# Initialize the GPS module
gpsd = gps(mode=gps.WATCH_ENABLE)

# Email Configuration
SMTP_SERVER = 'your_smtp_server'
SMTP_PORT = 587
SMTP_USERNAME = 'your_username'
SMTP_PASSWORD = 'your_password'
EMAIL_FROM = 'your_email@example.com'
EMAIL_TO = 'recipient@example.com'

# Paths for image files
CURRENT_IMAGE = '/home/pi/current_image.jpg'
PREVIOUS_IMAGE = '/home/pi/previous_image.jpg'

# Dummy Coordinates
DUMMY_LATITUDE = 18.463620852371374
DUMMY_LONGITUDE = 73.86815756783137

# Function to send an email with an image attachment
def send_email(image_filename, latitude, longitude):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = 'Emergency Alert: Urgent Help Needed!'

    # Check if GPS coordinates are valid; if not, use dummy coordinates
    if (latitude is None) or (longitude is None):
        latitude, longitude = DUMMY_LATITUDE, DUMMY_LONGITUDE

    # Attach text message with GPS coordinates and urgency
    message = f'Urgent help is needed!\n\n'
    message += f'Location: Latitude {latitude}, Longitude {longitude}\n\n'
    message += 'A person is in danger. Please respond immediately.'
    msg.attach(MIMEText(message))

    # Check if the image file exists
    if os.path.exists(image_filename):
        # Attach existing image
        with open(image_filename, 'rb') as image_file:
            image = MIMEImage(image_file.read(), name='emergency_image.jpg')
        msg.attach(image)
    else:
        # Attach a placeholder image or provide an alternative action
        with open('/home/pi/placeholder.jpg', 'rb') as image_file:
            image = MIMEImage(image_file.read(), name='placeholder_image.jpg')
        msg.attach(image)

    # Connect to SMTP server and send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

# Function to activate LEDs like a siren
def activate_siren_leds():
    while True:
        for led_pin in LED_PINS:
            GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.2)  # Delay to control LED blinking speed
        for led_pin in LED_PINS:
            GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.2)

# Main loop
try:
    while True:
        # Check if the Push Button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            # Activate the buzzer
            buzzer.start(50)  # 50% duty cycle
            time.sleep(1)     # Buzzer on for 1 second
            buzzer.stop()      # Turn off the buzzer

            # Activate the siren LEDs
            activate_siren_leds()

            # Check if a current image exists; if not, capture a new one
            if not os.path.exists(CURRENT_IMAGE):
                with picamera.PiCamera() as camera:
                    camera.capture(CURRENT_IMAGE)

            # Get GPS data
            packet = gpsd.next()
            if packet:
                latitude = packet['lat']
                longitude = packet['lon']

                # Send email with image and GPS data
                send_email(CURRENT_IMAGE, latitude, longitude)

                # Save the current image as the previous image
                os.rename(CURRENT_IMAGE, PREVIOUS_IMAGE)

                print("Emergency Alert Sent!")
                time.sleep(60)  # Delay to prevent continuous alerts
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
