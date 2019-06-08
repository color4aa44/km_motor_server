#!/bin/bash

BINDIR=$(cd $(dirname $0); pwd)

PYTHONPATH=$BINDIR

while :;
do
  $BINDIR/app.py
done
