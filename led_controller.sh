#!/bin/bash

# LED1
# 0bit : GPIO 5 (29pin)
# 1bit : GPIO 6 (31pin)
# 
# LED2
# 0bit : GPIO 13 (33pin)
# 1bit : GPIO 19 (35pin)
# 
# LED3
# 0bit : GPIO 20 (38pin)
# 1bit : GPIO 21 (40pin)

GPIO_DIR=/sys/class/gpio

LED1_0=5
LED1_1=6
LED1_0_F=/tmp/motor1_0
LED1_1_F=/tmp/motor1_1

echo 0 > $LED1_0_F
echo 0 > $LED1_1_F

LED2_0=13
LED2_1=19
LED2_0_F=/tmp/motor2_0
LED2_1_F=/tmp/motor2_1

echo 0 > $LED2_0_F
echo 0 > $LED2_1_F

LED3_0=20
LED3_1=21
LED3_0_F=/tmp/motor3_0
LED3_1_F=/tmp/motor3_1

echo 0 > $LED3_0_F
echo 0 > $LED3_1_F

led_setup() {
    echo $1 > $GPIO_DIR/export
    while ! [ -w $GPIO_DIR/gpio$1 ]
    do
        sleep 1
    done
    echo "GPIO$1 has setup"
    echo out > $GPIO_DIR/gpio$1/direction
}

led_setup $LED1_0
led_setup $LED1_1
led_setup $LED2_0
led_setup $LED2_1
led_setup $LED3_0
led_setup $LED3_1

led_on_of() {
    cat $1 > $GPIO_DIR/gpio$2/value
}

while :
do
    sleepenh 0.01 > /dev/null
    led_on_of $LED1_0_F $LED1_0
    led_on_of $LED1_1_F $LED1_1
    led_on_of $LED2_0_F $LED2_0
    led_on_of $LED2_1_F $LED2_1
    led_on_of $LED3_0_F $LED3_0
    led_on_of $LED3_1_F $LED3_1
done
