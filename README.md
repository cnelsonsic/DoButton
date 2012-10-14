DoButton
========

A button that makes your computer do things.

This project has two parts,
a python script that waits for communication on a serial port like "run the commands!",
and an arduino project that uses an LED pushbutton switch to both trigger the command
and to provide feedback as to the command's status (running, errored, done, etc.)

So, a user hits the button,
which makes the arduino tell the python script to run any executable files in ``~/.dobutton/``.

While the scripts are running, it tells the arduino to make the LED in the button slowly fade in and out.

When they succeed or fail, it sends that status back to the arduino to display it
as a solid light (good) or as a harshly blinking light (bad).

You can wire up the button by following the schematic (``DoButton_schem.png``) or opening it in Fritzing (``DoButton.fzz``).

The Arduino code is located in ``DoButton.pde``.
