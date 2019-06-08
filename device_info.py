#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#使用するモーターは固定なので型番、シリアル番号、MACアドレスは決め打ち
devices = {
    "motor1" : {
        "name" : "KM-1U",
        "serial" : "5DKW#736",
        "mac" : "e7:ed:c2:e4:b8:b1",
        "speed" : 1.0,
        "ini_rad" : 0.00,
        "min_rad" : -2.35,
        "max_rad" : 2.35,
        "remarks" : "base"
    },
    "motor2" : {
        "name" : "KM-1S", 
        "serial" : "7WSC#E82",
        "mac" : "c4:88:14:f4:e8:ad",
        "speed" : 0.8,
        "ini_rad" : 0.82,
        "min_rad" : 0.00,
        "max_rad" : 1.65,
        "remarks" : "joint"
    },
    "motor3" : {
        "name" : "KM-1S", 
        "serial" : "FEFZ#35F",
        "mac" : "cc:57:89:91:4e:5c",
        "speed" : 0.6,
        "ini_rad" : 0.0,
        "min_rad" : 0.0,
        "max_rad" : 6.28,
        "remarks" : "tip"
    }
}

