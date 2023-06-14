#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import GyroSensor, TouchSensor
from pybricks.parameters import Port, Button
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
sock.connect(("169.254.105.94",3020))
sock.settimeout(None)
global maxAngle
global ev3
ev3 = EV3Brick()
gyro = GyroSensor(Port.S3)
accelerator = TouchSensor(Port.S4)
decelarator = TouchSensor(Port.S1)

lastSent = -1
lastPressedA = False
lastPressedD = False
maxAngle = 80
sock.sendall("maxnagle"+str(maxAngle)+";")
debounceRight = False
debounceLeft = False

ev3.screen.clear()
ev3.screen.draw_text(0, 0, "Max Angle: "+str(maxAngle))
while True:
    if not Button.DOWN in ev3.buttons.pressed():
        if Button.CENTER in ev3.buttons.pressed():
            gyro.reset_angle(0)
        if Button.RIGHT in ev3.buttons.pressed():
            if not debounceRight:
                debounceRight = True
                maxAngle += 1
                sock.sendall("maxnagle"+str(maxAngle)+";")
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "Max Angle: "+str(maxAngle))
        else:
            debounceRight = False
        if Button.LEFT in ev3.buttons.pressed():
            if not debounceLeft:
                debounceLeft = True
                maxAngle -= 1
                sock.sendall("maxnagle"+str(maxAngle)+";")
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "Max Angle: "+str(maxAngle))
        else:
            debounceLeft = False
        angle = gyro.angle()
        pressedA = accelerator.pressed()
        pressedB = decelarator.pressed()
        
        sock.sendall("angle"+str(angle)+";")
        if pressedA != lastPressedA:
            sock.sendall("pressedA"+str(pressedA)+";")
            lastPressedA = pressedA
        if pressedB != lastPressedD:
            sock.sendall("pressedB"+str(pressedB)+";")
            lastPressedD = pressedB