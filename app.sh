#!/bin/bash

BINDIR=$(cd $(dirname $0); pwd)

PYTHONPATH=$BINDIR

$BINDIR/led_controller.sh &

while :;
do
  $BINDIR/server.py
done
