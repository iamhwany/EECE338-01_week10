import os
os.system("sudo pigpiod")

import time
import sys
import pigpio

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000

led_color = 0
last_tick = 0

def myISR(gpio, level, tick):
    global led_color, last_tick

    ## If it is not a button press
    if level != 0:
        return
    # Debouncing: Ignore if within 200ms of the last press
    if pigpio.tickDiff(last_tick, tick) < 200_000:
        return
    last_tick = tick

    # Check button status
    btn_state = pi.read(PIN_BTN)

    if btn_state == 0:
        # Color cycling (0~7)
        led_color = (led_color + 1) % 8
        # Control LED using RGB bit combinations (0 for ON, 1 for OFF)
        pi.write(PIN_LEDR, 0 if led_color & 0b100 else 1)
        pi.write(PIN_LEDG, 0 if led_color & 0b010 else 1)
        pi.write(PIN_LEDB, 0 if led_color & 0b001 else 1)
        # Output current color information
        print(f"[ISR] LED Color changed to {led_color:03b}")


if __name__ == "__main__":
    pi = pigpio.pi()
    if not pi.connected:
        print("pigpio demon error!", file=sys.stderr)
        sys.exit(1)

    # Set PIN_BTN to input mode
    pi.set_mode(PIN_BTN,  pigpio.INPUT)
    # Set the default state to HIGH by engaging the internal pull-up resistor -> LOW when the button is pressed
    pi.set_pull_up_down(PIN_BTN, pigpio.PUD_UP)

    pi.set_mode(PIN_LEDR, pigpio.OUTPUT)
    pi.set_mode(PIN_LEDG, pigpio.OUTPUT)
    pi.set_mode(PIN_LEDB, pigpio.OUTPUT)

    # Turn off all 3 LEDs (1 is off state; circuit turns on when LOW)
    pi.write(PIN_LEDR, 1)
    pi.write(PIN_LEDG, 1)
    pi.write(PIN_LEDB, 1)

    # When the button is pressed and a LOW signal is detected, call myISR
    cb = pi.callback(PIN_BTN, pigpio.FALLING_EDGE, myISR)

    print("!Interrupt!")
    count = 0
    try:
        while True:
            start = time.time()
            print(f"Current seconds: {count:4d} [s]")
            count += 2
            end = time.time()
            time.sleep((LOOP_PERIOD_MS/1000) - (end - start))
    finally:
        cb.cancel()
        pi.stop()
        os.system("sudo killall pigpiod")
