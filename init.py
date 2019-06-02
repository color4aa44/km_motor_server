#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# モーターをアームに取り付けた時に実行する。

import time

from pykeigan import blecontroller
from bluepy.btle import Scanner

import device_info

for device in device_info.devices.values()
    connection = blecontroller.BLEController(device["mac"])
    connection.enable_action()
    connection.preset_position(0)
    time.sleep(2)    
