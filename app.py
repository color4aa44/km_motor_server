#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import bluepy

from flask import Flask, request
from flask_socketio import SocketIO, emit
from pykeigan import blecontroller
from bluepy.btle import Scanner

import device_info

connections = {}

for key in device_info.devices:
    connections[key] = None

async_mode = None

app = Flask(__name__)

socket_io = SocketIO(app, async_mode=async_mode)

def connection_motor(key):
    device = device_info.devices[key]
    connection = blecontroller.BLEController(device["mac"])
    connection.enable_action()
    connection.enable_continual_imu_measurement()
    connection.stop_motor()
    connection.set_speed(device["speed"])
    connection.move_to_pos(device["ini_rad"])
    return connection

def fetch_motor():
    global connections
    while True:
        motor_info = {}
        for key, connection in connections.items():
            try:
                if connection == None:
                    connection = connection_motor(key)
                    connections[key] = connection
                    time.sleep(1)
                motor_info[key] = connection.read_motor_measurement()
                motor_info[key].update(connection.read_imu_measurement())
            except bluepy.btle.BTLEDisconnectError as e:
                connections[key] = None
            except Exception as e:
                print(e)
        socket_io.emit('fetch_motor', motor_info)
        time.sleep(1)

thread = None
#thread = socket_io.start_background_task(target=fetch_motor)

@socket_io.on('enable_fetch_motor', namespace='/motor')
def enable_fetch_motor():
    global thread
    if thread == None:
        thread = socket_io.start_background_task(target=fetch_motor)
    socket_io.emit("enable_controller", {})

@socket_io.on('connection', namespace='/motor')
def _connection(message):
    global connections
    if "id" not in message:
        print("err1")
        return
    if message["id"] not in device_info.devices:
        print("err2")
        return
    try:
        key = message["id"]
        connections[key] = connection_motor(key)
    except bluepy.btle.BTLEDisconnectError as e:
        connections[message["id"]] = None
        return
    except Exception as e:
        print(e)
        return

@socket_io.on('set_start_pos', namespace='/motor')
def set_start_pos(message):
    global connections
    for key, connection in connections.items():
        try:
            if connection == None:
                connection = connection_motor(key)
                connections[key] = connection
                time.sleep(1)
            connection.move_to_pos(device_info.devices[key]["ini_rad"])
        except bluepy.btle.BTLEDisconnectError as e:
            connections[key] = None
        except Exception as e:
            print(e)

#for key in device_info.devices:
#    _connection({"id" : key})
#    time.sleep(3)

def checkRadThreshold(rad, device):
    if rad < device["min_rad"]:
        return device["min_rad"]
    elif rad > device["max_rad"]:
        return device["max_rad"]
    else:
        return rad

@socket_io.on('rotate', namespace='/motor')
def rotate(message):
    global connections
    print(message)
    if "id" not in message:
        print("err1")
        return
    if "rad" not in message:
        print("err2")
        return 
    if message["id"] not in device_info.devices:
        print("err3")
        return
    device = device_info.devices[message["id"]]
    connection = connections[message["id"]]
    connection.move_to_pos(checkRadThreshold(message["rad"], device))

@socket_io.on('init_pos', namespace='/motor')
def init_pos():
    global connections
    for connection in connections.values():
        connection.preset_position(0)
        time.sleep(2)
    emit('init_pos_done')

socket_io.run(app, host='0.0.0.0', debug=True)
