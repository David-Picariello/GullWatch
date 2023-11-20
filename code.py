from adafruit_circuitplayground.express import cpx
import board
#import digitalio
import servo
import time
import neopixel
#import adafruit_motor.servo
import array
import math
import audiobusio
import pwmio
import analogio
#from adafruit_motor import servo
#import simpleio
#from adafruit_circuitplayground import cp


# Initialize a NeoPixel on pin A1 with 10 LEDs
led = neopixel.NeoPixel(board.NEOPIXEL, 10)

# Initialize a variable to control the alarm
stop_alarm = True

# servo
pwm = pwmio.PWMOut(board.A1, frequency=50)
motor_direction = 0
my_servo = servo.ContinuousServo(pwm, min_pulse=400, max_pulse=2500)

#Create the light sensor object to read from
light = analogio.AnalogIn(board.LIGHT)
#set lights and sound
def flash_leds_and_play_tone():
    while True:
        # cpx.play_file("alarm.wav")
        cpx.pixels.fill((200, 0, 0))
        cpx.play_tone(261.63, 0.5)
        cpx.pixels.fill((0, 0, 200))
        time.sleep(0.5)
# Sound Sensor
def mean(values):
    return sum(values) / len(values)
def normalized_rms(values):
    minbuf = int(mean(values))
    sum_of_samples = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )
    return math.sqrt(sum_of_samples / len(values))
mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16
)
samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))


while True:
    cpx.pixels.fill((0, 0, 0))
    my_servo.throttle = motor_direction
    if cpx.button_a:
        stop_alarm = True
        print("button a pressed")
    if cpx.button_b:
        stop_alarm = False
        print("button b pressed")

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    time.sleep(.1)
    print((light.value,))
    print((magnitude,))
    print((my_servo.throttle))
    if stop_alarm is True:
        if magnitude > 200 or light.value > 10:
            motor_direction = .15
            flash_leds_and_play_tone()
            #cpx.pixels.fill((0, 0, 0))


