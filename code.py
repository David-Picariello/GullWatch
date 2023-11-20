# SPDX-FileCopyrightText: 2018 Anne Barela for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from adafruit_circuitplayground.express import cpx
import array
import math
import audiobusio
import board
import time
import pwmio
from adafruit_motor import servo
# servo
pwm = pwmio.PWMOut(board.A1, frequency=50)
motor_direction = 0
my_servo = servo.ContinuousServo(pwm, min_pulse=400, max_pulse=2500)
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
# Countdown
def flash_leds_and_play_tone():
    for _ in range(3):
        cpx.pixels.fill((50, 0, 0))
        cpx.play_tone(261.63, 0.5)
        cpx.pixels.fill((0, 0, 0))
        time.sleep(0.5)
# LED control
def alternate_led_colors():
    num_leds = 10
    for i in range(num_leds):
        if i % 2 == 0:
            cpx.pixels[i] = (0, 20, 0)
        else:
            cpx.pixels[i] = (20, 0, 0)
    cpx.pixels.show()
    time.sleep(1)
    for i in range(num_leds):
        if i % 2 == 0:
            cpx.pixels[i] = (20, 0, 0)
        else:
            cpx.pixels[i] = (0, 20, 0)
    cpx.pixels.show()
    time.sleep(1)

while True:
    my_servo.throttle = motor_direction

    if cpx.switch:
        cpx.play_file("speed.wav")
        flash_leds_and_play_tone()
        cpx.pixels.fill((0, 50, 0))
        cpx.play_tone(440.00, 1)
        cpx.pixels.fill((0, 0, 0))
        motor_direction = 0.15

    if cpx.button_b:
        motor_direction = -1
        cpx.play_file("dip.wav")
        alternate_led_colors()

    if cpx.button_a:
        motor_direction = 1
        cpx.play_file("rise.wav")
        alternate_led_colors()

    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    time.sleep(.1)
    if magnitude > 400:
        motor_direction = 0
        cpx.pixels.fill((0, 0, 0))

