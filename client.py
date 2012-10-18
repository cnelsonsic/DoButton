#!/usr/bin/env python
from __future__ import print_function
import time
import os
import sys
import logging
import itertools

import serial
from serial.tools.list_ports import comports
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
    # print("Sending", msg.strip())
    assert s.write(msg) == len(msg)

def get_executable():
    '''Get all the executable files in ~/.dobutton/.'''
    return [x for x in sh.glob(os.path.expanduser(SCRIPTDIR+"/*")) if os.access(x, os.X_OK)]

def main():
    logger = logging.getLogger('dobutton')

    s = None
    while not s:
        for serial_dev in set(itertools.chain.from_iterable(comports())):
            try:
                # print("Trying {0}".format(serial_dev))
                s = serial.Serial(serial_dev, baudrate=9600, timeout=0.25)
                connected = False
                tries = 0
                while tries < 3:
                    if "IM A BUTTON" in s.readline():
                        # print("FOUND A BUTTON")
                        connected = True
                        while True:
                            write(s, SUCCESS)
                            time.sleep(.1)
                            if s.readline().strip() == "SUCCESS":
                                print("DoButton found!")
                                break
                        break
                    tries += 1
                else:
                    s.close()
                    continue

                if connected:
                    break
            except serial.serialutil.SerialException as exc:
                # Couldn't connect, skip it.
                # print("Couldn't connect to", serial_dev)
                # print(exc.message)
                continue
        else:
            # Tried all the devices, so sleep a bit before trying again.
            time.sleep(1)
            print(".", end='')
            sys.stdout.flush()

    # Get any button messages:
    while True:
        try:
            line = s.readline()
        except (OSError, serial.serialutil.SerialException, ValueError) as exc:
            # print(exc.message)
            # Arduino got unplugged, so start over.
            return main()

        if "PRESSED" in line:
            line = None
            # Send a message to the button that it's working.
            write(s, WORKING)

            # Call whatever script(s) are in ~/.dobutton/.
            for command in get_executable():
                try:
                    # Note: Don't background these, so they run in sequence
                    # and the "WORKING" message means something
                    print("Running", command)
                    run = sh.Command(command)
                    run()
                    print("Finished successfully.")
                except sh.ErrorReturnCode as exc:
                    # If any error in the executables...

                    # Log it
                    print(exc.message)
                    logger.error("ERROR: {0} exited with a nonzero exit status.".format(command))
                    logger.error(exc.stdout)
                    logger.error(exc.stderr)

                    # And inform the button.
                    write(s, ERROR)

                    # And give up running more commands.
                    break
            else:
                # When they're all done, and they all succeed, send the success message.
                write(s, SUCCESS)

if __name__ == "__main__":
    print("Trying to find a DoButton...", end="")
    main()
