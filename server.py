#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

from flask import Flask, request, abort, jsonify
from flask_restful import Api, Resource, url_for
from bluepy.btle import Scanner
from pykeigan import blecontroller

from device_info import devices

app = Flask(__name__)
api = Api(app)

dev_list = {}

for key in devices:
    dev_list[key] = None

class KMScan(Resource):
    def get(self):
        scanner = Scanner()
        devices = scanner.scan(5.0)
        device_info = []
        for dev in devices:
            for (adtype, desc, value) in dev.getScanData():
                if desc=="Complete Local Name" and "KM-1" in value:
                    info = {}
                    info["name"] = value
                    info["mac"] = dev.addr
                    device_info.append(info)
        return device_info

class KMInit(Resource):
    def get(self, id):
        global dev_list
        if id not in dev_list:
            abort(404)
        dev = blecontroller.BLEController(devices[id]["mac"])
        dev.enable_action()
        dev.preset_position(0)
        dev.disconnect()
        return {"result" : "ok"}

class KMConnection(Resource):
    def get(self, id):
        global dev_list
        if id not in dev_list:
            abort(404)
        if dev_list[id] != None:
            return {"result" : "ok"}
        device_info = devices[id]
        dev = blecontroller.BLEController(device_info["mac"])
        dev.enable_action()
        dev.stop_motor()
        dev.set_speed(device_info["speed"])
        dev.move_to_pos(device_info["ini_rad"])
        dev_list[id] = dev
        return {"result" : "ok"}

class KMRotate(Resource):
    def get(self, id, rad):
        global dev_list
        print(dev_list)
        if id not in dev_list:
            abort(404)
        dev = dev_list[id]
        device = devices[id]
        if dev == None:
            abort(403)
        rad_f = float(rad)
        if rad_f > device["max_rad"]:
            rad_f = device["max_rad"]
        elif rad_f < device["min_rad"]:
            rad_f = device["min_rad"]
        try:
            dev.move_to_pos(rad_f)
        except bluepy.btle.BTLEDissconnectError as e:
            dev = blecontroller.BLEController(device["mac"])        
            dev.stop_motor()
            dev.move_to_pos(rad_f)
            dev_list[id] = dev
        except Exception as e:
            print(e)
            abort(500)
        return {"result" : "ok"}

class KMFetchMotorInfo(Resource):
    def get(self, id):
        global dev_list
        if id not in dev_list:
            abort(404)
        dev = dev_list[id]
        device = devices[id]
        if dev == None:
            abort(403)
        try:
            return dev.read_motor_measurement()
        except bluepy.btle.BTLEDisconnectError as e:
            dev = blecontroller.BLEController(device["mac"])
            dev.stop_motor()
            dev_list[id] = dev
            return dev.read_motor_measurement()
        except Exception as e:
            print(e)
            abort(500)
        

api.add_resource(KMScan, '/api/scan')
api.add_resource(KMInit, '/api/init/<string:id>')
api.add_resource(KMConnection, '/api/connection/<string:id>')
api.add_resource(KMRotate, '/api/rotate/<string:id>/rad/<string:rad>')
api.add_resource(KMFetchMotorInfo, '/api/fetch/<string:id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10080)
