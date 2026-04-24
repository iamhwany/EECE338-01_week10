from gpiozero import Button, LED
import time

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000

# Start at state 7 (111 in binary), which matches the 'Off' state in your image
led_val = 7

# Setup LEDs.
# We use default active_high=True so that .value = 1 outputs HIGH (LED OFF)
# and .value = 0 outputs LOW (LED ON). This perfectly matches your (111) to (000) logic.
led_r = LED(PIN_LEDR)
led_g = LED(PIN_LEDG)
led_b = LED(PIN_LEDB)

# Initial state (111 -> Off)
led_r.value = 1
led_g.value = 1
led_b.value = 1

# Button Setup: Internal pull-up, 200ms debouncing
btn = Button(PIN_BTN, pull_up=True, bounce_time=0.2)

def myISR():
    """Callback function to be executed on button press"""
    global led_val

    ################ Write Codes From Here ################

    #######################################################

    print(f"[ISR] LED Color changed to {led_r.value}{led_g.value}{led_b.value}")

# Register Interrupt
btn.when_pressed = myISR

if __name__ == "__main__":
    print("!Interrupt Ready!")
    count = 0
    try:
        while True:
            start = time.time()
            print(f"Current seconds: {count:4d} [s]")
            count += 2
            end = time.time()

            # Maintain loop period
            sleep_time = (LOOP_PERIOD_MS / 1000.0) - (end - start)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nProgram exiting...")
    finally:
        # Clean up resources
        led_r.close()
        led_g.close()
        led_b.close()
        btn.close()