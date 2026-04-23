from gpiozero import Button, RGBLED
import time

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000
led_color = 0

# 1. LED Setup: active_high=False (Circuit turns on at LOW signal)
led = RGBLED(red=PIN_LEDR, green=PIN_LEDG, blue=PIN_LEDB, active_high=False)
# Initial state: Turn off all LEDs
led.off()

# 2. Button Setup: Internal pull-up (pull_up=True), 200ms debouncing (bounce_time=0.2)
btn = Button(PIN_BTN, pull_up=True, bounce_time=0.2)

def myISR():
    """Callback function to be executed on button press (Falling Edge)"""
    global led_color

    # Color cycling (0~7)
    led_color = (led_color + 1) % 8

    # Determine status via bitwise operations: 0b100(R), 0b010(G), 0b001(B)
    # RGBLED in gpiozero accepts values from 0 (Off) to 1 (On)
    r_val = 1 if (led_color & 0b100) else 0
    g_val = 1 if (led_color & 0b010) else 0
    b_val = 1 if (led_color & 0b001) else 0

    led.color = (r_val, g_val, b_val)
    print(f"[ISR] LED Color changed to {led_color:03b}")

# 3. Register myISR to be called when the button is pressed (Interrupt)
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

            # Maintain loop period (compensating for execution time)
            sleep_time = (LOOP_PERIOD_MS / 1000.0) - (end - start)
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nProgram exiting...")
    finally:
        # Turn off the LED and clean up resources upon exit
        led.close()
        btn.close()