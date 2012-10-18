const int VERSION = 1;
const int SPEED = 9600;
const int BUTTON_DEBOUNCE = 1; // Seconds.

// These are sent to the PC over serial and can be used to identify a DoButton.
const String HELO = "IM A BUTTON";
const String ACTION = "PRESSED";

// These come in from the PC to tell us what's up.
const String WORKING = "WORKING";
const String ERROR = "ERROR";
const String SUCCESS = "SUCCESS";

// LED States
const int OFF = 0;
const int ON = 1;
const int THROBBING = 2;
const int FLASHING = 3;
int LED_STATE;

// Pin Settings
const int LED_PIN = 5;
const int BUTTON_PIN = 2;

// Global LED timing variables.
int _led_state = 0; // Current logical state of the LED.
int _led_direction = 1; // Are we getting brighter or dimmer?
long _previous_millis = 0; // The last time the LED was updated.

// Global Button state variables.
long _last_press = 0; // The last time the button was pressed.

String getString() {
    int i = 0;
    char commandbuffer[20];

    if (Serial.available()) {
        delay(100);
        while (Serial.available() && i < 19) {
            commandbuffer[i++] = Serial.read();
        }
        commandbuffer[i++] = '\0';
    }

    if (i > 0) {
        return String((char*)commandbuffer);
    }
}

void setup() {
    // Initialize our LED
    LED_STATE = OFF;
    /* pinMode(LED_PIN, OUTPUT); */
    pinMode(BUTTON_PIN, INPUT);

    // Enable serial communication.
    Serial.begin(SPEED);
    Serial.flush();
}

// Handle button press stuff.
void loop() {
    notify();
    handleLED();
    handleButton();
}

long _last_notify;
void notify() {
    // Notify the PC every second or so that we're a button.
    unsigned long currentMillis = millis();
    if (currentMillis - _last_notify > BUTTON_DEBOUNCE*1000) {
        _last_notify = currentMillis;
        Serial.println(HELO);
    }
}

void handleLED() {
    // Do LED stuff to throb/flash/turn on/off LED.
    if (LED_STATE == THROBBING) {
        fade(1, 1);
    }
    else if (LED_STATE == FLASHING) {
        fade(255, 500);
    }
    else if (LED_STATE == ON) {
        analogWrite(LED_PIN, 255);
    }
    else if (LED_STATE == OFF) {
        analogWrite(LED_PIN, 0);
    }
}

void fade(int amount, int interval) {
  unsigned long currentMillis = millis();
  if (currentMillis - _previous_millis > interval) {
    // save the last time you blinked the LED
    _previous_millis = currentMillis;

    // Update the direction of the LED brightening/dimming.
    if (_led_state <= 0) {
        _led_direction = 1;
    }
    else if (_led_state >= 255) {
        _led_direction = -1;
    }

    _led_state += (_led_direction * amount);
    analogWrite(LED_PIN, constrain(_led_state, 0, 255));
    delay(10);
  }
}

void handleButton() {
    // When pressed, send "PRESSED" via serial
    if (digitalRead(BUTTON_PIN) == HIGH) {
        // But only if the client's not busy.
        if (LED_STATE != THROBBING) {
            // And only if we're not hammering the button.
            if (_last_press <= (millis() - 1000)) {
                Serial.println(ACTION);
                _last_press = millis();
            }
        }
    }
}

void setState(int state) {
    LED_STATE = state;
    _led_state = 0; // When we change states, reset the LED brightness to 0.
}

// Handle serial stuff.
void serialEvent() {
    // Got some data from the PC
    String result = getString();
    if (result == WORKING) {
        // If it's "WORKING", initiate LED throbbing protocol.
        setState(THROBBING);
        Serial.println("THROBBING");
    }
    else if (result == ERROR) {
        // If it's "ERROR", flash the LED.
        setState(FLASHING);
        Serial.println("FLASHING");
    }
    else if (result == SUCCESS) {
        // If it's "SUCCESS", set the LED to a constant on state.
        setState(ON);
        Serial.println("SUCCESS");
    }
    else {
        // Do nothing with it, but advise the client that we're confused.
        Serial.print("UNRECOGNIZED INPUT:");
        Serial.println(result);
    }
}
