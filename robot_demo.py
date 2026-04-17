import gpiozero

start_button = gpiozero.Button()

next_button = gpiozero.Button()

stop_button = gpiozero.Button()

gpio_pins = [14, 15, 18, 23, 24, 25, 8, 7]

relay_pins = [gpiozero.DigitalOutputDevice(pin=pin, active_high=True, initial_value=False) for pin in gpio_pins]

# wait for barcode scan and start signal

# run through 3 positions for part 1

# wait for flip button

# run through last three positions for part 1

# update csv with data

# wait for barcode scan and start signal

# go to position 1

# update csv with defect and send email

# wait for barcode scan and start signal

# go to position 1

# update csv with defect and send email

# wait for barcode scan and start signal

# go to position 1

# update csv with defect and send email

# wait for barcode scan until end of time