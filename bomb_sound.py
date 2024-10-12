import machine
from machine import Pin, PWM
import time
from bomb_display import greeting

def beeping():
    # Set GPIO 28 as a PWM pin for the buzzer
    buzzer_pin = 28
    pwm_buzzer = PWM(Pin(28))
    pwm_buzzer = PWM(Pin(buzzer_pin))
    # Set the initial PWM frequency
    pwm_buzzer.freq(1000)

    # Function to calculate the duty cycle based on fComplete
    def calculate_duty_cycle(fComplete):
        fComplete = max(0, min(fComplete, 1))
        return int(max(0.1 + 0.9 * fComplete, 0.15) * 65535)

    # Function to handle the beeping with fixed pulse length
    def beep_with_fixed_pulse_length(fComplete):
        duty = calculate_duty_cycle(fComplete)
        pwm_buzzer.duty_u16(duty)
        time.sleep(0.15)
        pwm_buzzer.duty_u16(0)

    # Function for frequency sweep from 700 to 1500 Hz
    def sweep_frequency(duration):
        pwm_buzzer.duty_u16(49152)  # Set duty cycle to 75% (49152 out of 65535)
        steps = 100  # Increase number of steps for smoother transition
        for i in range(steps):
            freq = 700 + int((i / steps) * (1500 - 700))  # Calculate current frequency
            pwm_buzzer.freq(freq)
            print(f'Setting frequency: {freq} Hz')
            time.sleep(duration / steps)  # Delay for each step to allow hearing

    # Function for 8 beeps
    def beep_sequence():
        for _ in range(10):
            pwm_buzzer.duty_u16(32768)  # 50% duty cycle
            time.sleep(0.05)  # Beep duration
            pwm_buzzer.duty_u16(0)  # Turn off buzzer
            time.sleep(0.05)  # Gap between beeps

    # Total duration to run (in seconds)
    total_duration = 40
    start_time = time.time()
    x=67

    # Simulate fComplete from 0 to 1 (progression over time)
    while time.time() - start_time < total_duration:
        elapsed_time = time.time() - start_time
        fComplete = min(elapsed_time / total_duration, 1.0)

        beep_with_fixed_pulse_length(fComplete)
        
        gap_time = max(0.05, 1.0 - (fComplete * 0.95))
        time.sleep(gap_time)
        x -= 1
        greeting(str(x))

    # Ensure the buzzer is off after the loop ends
    pwm_buzzer.duty_u16(10)

    # Sweep frequency from 700 to 1500 Hz over 3 seconds
    sweep_frequency(2)

    # Ensure the buzzer is off after the sweeping ends
    pwm_buzzer.duty_u16(10)

    # Play the sequence of 8 beeps
    beep_sequence()

    # Ensure the buzzer is off after the beeping sequence ends
    pwm_buzzer.duty_u16(0)
