import serial
import time
import os

for serial_dev in [dev for dev in os.listdir('/dev/') if 'usb' in dev]:
    try:
        s = serial.Serial('/dev/'+serial_dev, 9600)
        if "IM A BUTTON" in s.readline():
            break
    except serial.serialutil.SerialException as exc:
        # Couldn't connect, skip it.
        print "Couldn't connect to", serial_dev
        print exc.message
        continue

def write(s, msg):
    print "Sending", msg.strip()
    assert s.write(msg) == len(msg)

for cmd, result in {"WORKING": "THROBBING", "SUCCESS": "SUCCESS", "ERROR": "FLASHING"}.iteritems():
    while True:
        line = s.readline()
        if "IM A BUTTON" in line:
            write(s, cmd)
        else:
            if result in line:
                print "GOT WHAT WE WANTED:", result
                break
            else:
                print line.strip()
    print "Sleeping"
    time.sleep(10)

