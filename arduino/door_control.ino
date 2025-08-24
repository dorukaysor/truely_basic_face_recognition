#include <Servo.h>

Servo doorServo;
int irPin = 2;        // IR sensor connected to D2
int servoPin = 9;     // Servo to D9
char cmd;

void setup() {
  Serial.begin(9600);
  pinMode(irPin, INPUT);
  doorServo.attach(servoPin);
  doorServo.write(0); // door closed
}

void loop() {
  // Detect presence
  if (digitalRead(irPin) == HIGH) {
    Serial.println("P");  // send presence to Pi
    delay(1000);
  }

  // Listen for Pi command
  if (Serial.available() > 0) {
    cmd = Serial.read();
    if (cmd == 'O') {
      doorServo.write(90); // open door
      delay(5000);         // wait
      doorServo.write(0);  // close door
    }
  }
}