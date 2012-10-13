DoButton
========

A button that makes your computer do things.

This project has two parts,
a script that waits for communication on a serial port like "do the command!",
and an arduino project that uses an LED pushbutton switch to both trigger the command
and to provide feedback as to the command's status (running, errored, done, etc.)

You can wire up the button by following the schematic (``DoButton_schem.png``) or opening it in Fritzing (``DoButton.fzz``).

The Arduino code is located in ``DoButton.pde``.
