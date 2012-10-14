#!/usr/bin/env python
from __future__ import print_function
import serial
import time
import os
import sys
import sh

SCRIPTDIR = "~/.dobutton/"

WORKING = "WORKING"
SUCCESS = "SUCCESS"
ERROR = "ERROR"

def test(s):
    command_results = {WORKING: "THROBBING",
                       SUCCESS: "SUCCESS",
                       ERROR: "FLASHING"}

    for cmd, result in command_results.iteritems():
        while True:
            line = s.readline()
            if "IM A BUTTON" in line:
                write(s, cmd)
            else:
                if result in line:
                    print("GOT WHAT WE WANTED:", result)
                    break
                else:
                    print(line.strip())
        time.sleep(10)

def write(s, msg):
    print("Sending", msg.strip())
    assert s.write(msg) == len(msg)

def get_executable():
    '''Get all the executable files in ~/.dobutton/.'''
    return [x for x in sh.glob(os.path.expanduser(SCRIPTDIR+"/*")) if os.access(x, os.X_OK)]

def main():
    s = None
    while not s:
        for serial_dev in [dev for dev in os.listdir('/dev/') if 'usb' in dev]:
            try:
                s = serial.Serial('/dev/'+serial_dev, baudrate=9600, timeout=2)
                if "IM A BUTTON" in s.readline():
                    break
            except serial.serialutil.SerialException as exc:
                # Couldn't connect, skip it.
                print("Couldn't connect to", serial_dev)
                print(exc.message)
                continue
        else:
            # Tried all the devices, so sleep a bit before trying again.
            time.sleep(1)
            print(".", end='')
            sys.stdout.flush()
    print("Connected to arduino.")

    # Get any button messages:
    while True:
        line = s.readline()
        if "PRESSED" in line:
            # Send a message to the button that it's working.
            write(s, WORKING)

            # Call whatever script(s) are in ~/.dobutton/.
            for command in get_executable():
                try:
                    # Note: Don't background these, so they run in sequence
                    # and the "WORKING" message means something
                    print("running", command)
                    run = sh.Command(command)
                    run()
                except sh.ErrorReturnCode as exc:
                    # If any error, send the error message and abandon the rest of the commands.
                    print(exc.message)
                    write(s, ERROR)
                    break
            else:
                # When they're all done, and they all succeed, send the success message.
                write(s, SUCCESS)

if __name__ == "__main__":
    main()
