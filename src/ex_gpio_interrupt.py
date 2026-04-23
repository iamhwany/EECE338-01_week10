from gpiozero import Button, LED
import time

PIN_BTN  = 14
PIN_LEDR = 16
PIN_LEDG = 20
PIN_LEDB = 21

LOOP_PERIOD_MS = 2000
led_color = 0

# 1. Individual LED Setup: active_high=False (Circuit turns on at LOW signal)
# Using individual LEDs instead of RGBLED to avoid PWM compatibility issues on RPi 5
led_r = LED(PIN_LEDR, active_high=False)
led_g = LED(PIN_LEDG, active_high=False)
led_b = LED(PIN_LEDB, active_high=False)

# Initial state: Turn off all LEDs
led_r.off()
led_g.off()
led_b.off()

# 2. Button Setup: Internal pull-up (pull_up=True), 200ms debouncing (bounce_time=0.2)
btn = Button(PIN_BTN, pull_up=True, bounce_time=0.2)

def myISR():
    """Callback function to be executed on button press (Falling Edge)"""
    global led_color

    # Color cycling (0~7)
    led_color = (led_color + 1) % 8

    # Turn LEDs on/off based on bitwise operations: 0b100(R), 0b010(G), 0b001(B)
    if led_color & 0b100: led_r.on()
    else: led_r.off()

    if led_color & 0b010: led_g.on()
    else: led_g.off()

    if led_color & 0b001: led_b.on()
    else: led_b.off()

    print(f"[ISR] LED Color changed to {led_color:03b}")

# 3. Register myISR to be called when the button is pressed (Interrupt)
btn.when_pressed = myISR

if __name__ == "__main__":
    print("!Interrupt!")
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
        # Turn off the LEDs and clean up resources upon exit
        led_r.close()
        led_g.close()
        led_b.close()
        btn.close()