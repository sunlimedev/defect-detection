import gpiozero
import cv2
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

RETRY_DELAY = config.barcode_scanner.retry_delay
SCANNER_DEVICE_ID = config.barcode_scanner.device_id

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






# wait for barcode scan and start signal
serial_number1 = read_barcode(SCANNER_DEVICE_ID)

# run through 3 positions for part 1 (pulse 101)
start_led.blink()
while not start_btn.is_held:
    continue
start_led.off()
prog1_led.on()

relay_start.on()
time.sleep(0.02)
realy_start.off()
time.sleep(10)

for _ in range(3):
    relay_next.on()
    time.sleep(0.02)
    relay_next.off()
    time.sleep(10)

# wait for flip button
flip_led.blink()
while not flip_btn.is_help:
    continue
prog1_led.off()
flip_led.off()
prog2_led.on()

# run through last three positions for part 1
for _ in range(3):
    relay_next.on()
    time.sleep(0.02)
    relay_next.off()
    time.sleep(10)

# first part good
prog2_led.off()
good_led.on()



# update csv with data and send email (good part)
#send_email(serial_number1, 0, "no_defect")



# wait for barcode scan and start signal
serial_number2 = read_barcode(SCANNER_DEVICE_ID)
start_led.blink()
while not start_btn.is_held:
    continue
good_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_start.on()
time.sleep(0.02)
relay_start.off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (squircle discoloration)
#send_email(serial_number2, 1, "discoloration")



# wait for barcode scan and start signal
serial_number3 = read_barcode(SCANNER_DEVICE_ID)
start_led.blink()
while not start_btn.is_held:
    continue
defective_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_start.on()
time.sleep(0.02)
relay_start.off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (rectangle scratch)
#send_email(serial_number3, 1, "scratch")



# wait for barcode scan and start signal
serial_number4 = read_barcode(SCANNER_DEVICE_ID)
start_led.blink()
while not start_btn.is_held:
    continue
defective_led.off()
start_led.off()
prog1_led.on()

# go to position 1
relay_start.on()
time.sleep(0.02)
relay_start.off()
time.sleep(7)
prog1_led.off()
defective_led.on()



# update csv with defect and send email (square dent)
#send_email(serial_number4, 1, "dent")