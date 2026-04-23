from gpiozero import Button, LED
import time

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000
led_color = 0

# 1. Individual LED Setup: active_high=False (Circuit turns on at LOW signal)
led_r = LED(PIN_LEDR, active_high=False)
led_g = LED(PIN_LEDG, active_high=False)
led_b = LED(PIN_LEDB, active_high=False)

# Initial state: Turn off all LEDs
led_r.off()
led_g.off()
led_b.off()

# 2. Button Setup: Internal pull-up (pull_up=True)
btn = Button(PIN_BTN, pull_up=True)

def change_color():
    """Function to change LED colors based on current state"""
    global led_color

    # Color cycling: 0 -> 7
    led_color = (led_color + 1) % 8

    # Control LEDs by mapping each bit to R/G/B
    if led_color & 0b100: led_r.on()
    else: led_r.off()

    if led_color & 0b010: led_g.on()
    else: led_g.off()

    if led_color & 0b001: led_b.on()
    else: led_b.off()

    # Console output (color information)
    print(f"[Polling] LED Color: {led_color:03b}")

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