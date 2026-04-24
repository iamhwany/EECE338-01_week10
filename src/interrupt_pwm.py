from gpiozero import Button, LED
import signal
import time

PIN_BTN  = 14
PIN_LEDR = 16

# Setup LED and Button
led_r = LED(PIN_LEDR, active_high=False)
led_r.off()
btn = Button(PIN_BTN, pull_up=True, bounce_time=0.2)

# PWM Variables
# pwm_counter: counts from 0 to 9 to create a 10-step PWM period
# duty_cycle: threshold to turn the LED on or off
pwm_counter = 0
duty_cycle = 2

def btn_isr():
    """Button Interrupt: Changes the duty cycle"""
    global duty_cycle

    ################ Write Codes From Here ################
    # Goal: Change the duty_cycle when the button is pressed.
    # Cycle through the following values: 2 -> 5 -> 10 -> 2 ...
    # (This corresponds to 20% -> 50% -> 100% brightness)





    #######################################################

    print(f"[Button ISR] Brightness changed to: {duty_cycle * 10}%")

btn.when_pressed = btn_isr

def timer_isr(signum, frame):
    """Timer Interrupt: Executes every 1ms to generate Software PWM"""
    global pwm_counter

    ################ Write Codes From Here ################
    # Goal 1: Increase the pwm_counter by 1.
    # If the counter reaches 10, reset it to 0.



    # Goal 2: Compare pwm_counter with duty_cycle.
    # Turn the LED ON if counter is less than duty_cycle.
    # Otherwise, turn the LED OFF.




    #######################################################

# Set up Timer Interrupt (1ms interval)
signal.signal(signal.SIGALRM, timer_isr)
signal.setitimer(signal.ITIMER_REAL, 0.001, 0.001)

if __name__ == "__main__":
    print("!Software PWM using Timer Interrupt Ready!")
    print("Press the button to change brightness (20% -> 50% -> 80% -> 100%)")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram exiting...")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        led_r.close()
        btn.close()