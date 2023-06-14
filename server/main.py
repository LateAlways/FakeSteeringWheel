import socket
import vgamepad as vg

gamepad = vg.VX360Gamepad()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind(("",3020))

sock.listen(1)

while True:

    connection,address = sock.accept()
    connection.settimeout(3600)

    boolEnd = False
    while not boolEnd:
        try:
            maxAngle = 80
            received = connection.recv(1024).decode()
            if received != "":
                messages = received.split(";")
                for message in messages:
                    if "maxnagle" in message:
                        maxAngle = int(message.replace("maxnagle", ""))
                    if "angle" in message:
                        angle = int(message.replace("angle", ""))

                        twidth = max(min(angle/maxAngle, 1), -1)
                        twidth = int(twidth * 32767)
                        gamepad.left_joystick(x_value=twidth, y_value=0)
                    if "pressedA" in message:
                        pressed = message.replace("pressedA", "") == "True"
                        if pressed:
                            gamepad.right_trigger_float(value_float=1)
                        else:
                            gamepad.right_trigger_float(value_float=0)
                    if "pressedB" in message:
                        pressed = message.replace("pressedB", "") == "True"
                        if pressed:
                            gamepad.left_trigger_float(value_float=1)
                        else:
                            gamepad.left_trigger_float(value_float=0)

            gamepad.update()
        except socket.timeout:
            print("Connection timed out.")
            boolEnd = True