int VERSION = 1;
int SPEED = 9600;

// These are sent to the PC over serial and can be used to identify a DoButton.
String HELO = "IM A BUTTON";
String ACTION = "PRESSED";

// These come in from the PC to tell us what's up.
String WORKING = "IN PROGRESS";
String ERROR = "ERROR";
String SUCCESS = "SUCCESS";

// LED States
int LED_STATE;
int OFF = 0;
int ON = 1;
int THROBBING = 2;
int FLASHING = 3;

String getString() {
    String content = "";
    char character;

    while(Serial.available()) {
        character = Serial.read();
        content.concat(character);
    }
    return content;
}

void setup() {
    // Initialize our LED
    LED_STATE = OFF;

    // Enable serial communication.
   Serial.begin(SPEED);
   Serial.println(HELO);
}

// Handle button press stuff.
void loop() {
    handleLED();
    handleButton();
}

void handleLED() {
    // Do LED stuff to throb/flash/turn on/off LED.
}

void handleButton() {
    // Wait for button-press
    // When pressed, send "PRESSED" via serial
    // If not pressed, send "IM A BUTTON" once every second.
}

// Handle serial stuff.
void serialEvent() {
    // Got some data from the PC
    String result = getString();
    if (result == WORKING) {
        // If it's "IN PROGRESS", initiate LED throbbing protocol.
        LED_STATE = THROBBING;
    }
    else if (result == ERROR) {
        // If it's "ERROR", flash the LED.
        LED_STATE = FLASHING;
    }
    else if (result == SUCCESS) {
        // If it's "SUCCESS", set the LED to a constant on state.
        LED_STATE = ON;
    }
    else {
        // Do nothing with it, but advise the client that we're confused.
        Serial.print("UNRECOGNIZED INPUT:");
        Serial.println(result);
    }
}
