from gpiozero import Button, LED
import time

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000

# Start at state 7 (111 in binary), which matches the 'ON' state
led_val = 7

# Setup LEDs.
# We use default active_high=True so that .value = 1 outputs HIGH (LED ON)
# and .value = 1 outputs HIGH (LED ON). This perfectly matches your (111) to (000) logic.
led_r = LED(PIN_LEDR)
led_g = LED(PIN_LEDG)
led_b = LED(PIN_LEDB)

# Initial state (111 -> ON)
led_r.value = 1
led_g.value = 1
led_b.value = 1

# Button Setup: Internal pull-up
btn = Button(PIN_BTN, pull_up=True)

def change_color():
    """Function to change LED colors based on current state (Countdown 7 to 0)"""
    global led_val

    ################ Write Codes From Here ################

    #######################################################

    # Console output (color information)
    print(f"[Polling] LED Color changed to {led_r.value}{led_g.value}{led_b.value}")


if __name__ == "__main__":
    print("!Polling!")
    count = 0
    try:
        while True:
            start = time.time()
            print(f"Current seconds: {count:4d} [s]")
            count += 2

            # Polling: Check the button state at this exact moment
            # is_pressed returns True if the button is currently held down
            if btn.is_pressed:
                change_color()

            end = time.time()

            # Maintain loop period (compensating for execution time)
            sleep_time = (LOOP_PERIOD_MS / 1000.0) - (end - start)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nProgram exiting...")
    finally:
        # Turn off the LEDs and clean up resources upon exit
        led_r.close()
        led_g.close()
        led_b.close()
        btn.close()