import datetime

import RPi.GPIO as GPIO


def speed_test():
    start = datetime.datetime.now()
    x = 0
    for i in range(1000 * 1000):
        x += 1
    stop = datetime.datetime.now()
    duration = stop - start
    print(duration, x)


def speed_test2(pin, other=None):
    GPIO.setup(pin, GPIO.OUT)
    if other is None:
        other = pin
    else:
        GPIO.setup(other, GPIO.OUT)
    start = datetime.datetime.now()
    x = 0
    for i in range(80 * 1000):
        GPIO.output(pin, 1)
        x += 1
        GPIO.output(pin, 0)
        GPIO.output(other, 1)
        GPIO.output(other, 0)
        GPIO.output(pin, 1)
        GPIO.output(pin, 0)

    stop = datetime.datetime.now()
    duration = stop - start
    print(duration, x)


def main():
    print('hello')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    speed_test2(24, 26)
    print('goodbye')


if __name__ == '__main__':
    main()
