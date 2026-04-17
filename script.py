import gpiozero
import os
import time
from evdev import InputDevice, ecodes

# relay pins
gpio_pins = [14, 15, 18, 23, 24, 25, 8, 7]
relay_pins = [gpiozero.DigitalOutputDevice(pin=pin, active_high=True, initial_value=False) for pin in gpio_pins]

# all buttons and LEDs
start_led = gpiozero.LED(2)
prog1_led = gpiozero.LED(3)
flip_led = gpiozero.LED(4)
prog2_led = gpiozero.LED(17)
good_led = gpiozero.LED(27)
defective_led = gpiozero.LED(22)
start_btn_led = gpiozero.LED(10)
flip_btn_led = gpiozero.LED(9)
start_btn = gpiozero.Button(13)
flip_btn = gpiozero.Button(19)
stop_btn = gpiozero.Button(26)

RETRY_DELAY = 5.0
SCANNER_DEVICE_ID = "/dev/input/by-id/usb-NetChip_HID_Gadget_20080411-event-kbd"

def read_barcode(device_path=SCANNER_DEVICE_ID):
    """Read barcode from the specified input device. Blocking until barcode is read. Retries if the device is unavailable."""
    #TODO maybe add max retries?
    while True:  # retry forever
        try:
            dev = InputDevice(device_path)
            barcode = ""

            for event in dev.read_loop():
                if event.type != ecodes.EV_KEY or event.value != 1:
                    continue

                key = ecodes.KEY[event.code]

                if key == "KEY_ENTER":
                    if barcode:
                        return barcode
                    barcode = ""

                elif key.startswith("KEY_"):
                    char = key.replace("KEY_", "")
                    if len(char) == 1:
                        barcode += char
                    elif char == "MINUS":
                        barcode += "-"

        except OSError as e:
            # Device disconnected / reset
            print(f"Scanner unavailable, retrying in {RETRY_DELAY}s ({e})")
            time.sleep(RETRY_DELAY)


import smtplib
import ssl
from email.message import EmailMessage
import os
EMAIL_SENDER = "part.defect.notification@gmail.com"
EMAIL_PASSWORD = "zvod nwrs muxd kidc"
EMAIL_RECEIVER_LIST = ["apr6001@psu.edu"]
INCLUDE_PICTURES = True

def send_email(subject,content,pictures=None):
    """Send an email with the given content to the receiver list in config."""


    if not EMAIL_SENDER or not EMAIL_PASSWORD or EMAIL_RECEIVER_LIST == [""]:
        print("Email config is incomplete. Skipping email sending.")
        return

    # Create the email message object
    em = EmailMessage()
    em.set_content(content)
    em['Subject'] = subject
    em['From'] = EMAIL_SENDER
    em['Bcc'] = ', '.join(EMAIL_RECEIVER_LIST) # Use Bcc to hide recipient list

    if INCLUDE_PICTURES and pictures:
        for picture in pictures:
            try:
                with open(picture, 'rb') as img:
                    img_data = img.read()
                    em.add_attachment(img_data, maintype='image', subtype='jpeg', filename=os.path.basename(picture))
            except Exception as e:
                print(f"Error attaching picture {picture}: {e}")

    # Connect to the SMTP server and send
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(em)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Email Error: {e}")



# wait for barcode scan and start signal
serial_number1 = read_barcode()

# run through 3 positions for part 1 (pulse 101)
start_led.blink()
while not start_btn.is_held:
    continue
start_led.off()
prog1_led.on()

relay_pins[0].on()
time.sleep(0.02)
relay_pins[1].off()
time.sleep(8)

for _ in range(6):
    relay_pins[1].on()
    time.sleep(0.02)
    relay_pins[1].off()
    time.sleep(8)

# wait for flip button
flip_led.blink()
while not flip_btn.is_held:
    continue
prog1_led.off()
flip_led.off()
prog2_led.on()

# run through last three positions for part 1
for _ in range(6):
    relay_pins[1].on()
    time.sleep(0.02)
    relay_pins[1].off()
    time.sleep(8)

# first part good
prog2_led.off()
good_led.on()



# update csv with data 



# wait for barcode scan and start signal
serial_number2 = read_barcode()
start_led.blink()
while not start_btn.is_held:
    continue
good_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_pins[1].on()
time.sleep(0.02)
relay_pins[1].off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (squircle discoloration)
content = f"Defect detected in squircle part {serial_number2} - discoloration."
send_email(f"Defect Detected: {serial_number2}", content, None)



# wait for barcode scan and start signal
serial_number3 = read_barcode()
start_led.blink()
while not start_btn.is_held:
    continue
defective_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_pins[1].on()
time.sleep(0.02)
relay_pins[1].off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (rectangle scratch)
content = f"Defect detected in rectangle part {serial_number3} - scratch."
send_email(f"Defect Detected: {serial_number3}", content, None)



# wait for barcode scan and start signal
serial_number4 = read_barcode()
start_led.blink()
while not start_btn.is_held:
    continue
defective_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_pins[1].on()
time.sleep(0.02)
relay_pins[1].off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (square dent)
content = f"Defect detected in square part {serial_number4} - dent."
send_email(f"Defect Detected: {serial_number4}", content, None)


time.sleep(100)
