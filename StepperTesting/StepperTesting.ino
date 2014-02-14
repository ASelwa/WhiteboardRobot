
// initialize variables
int stepR = 13;
int dirR = 12;
int stepL = 1;
int dirL = 0;

int speedR1 = 9;
int speedR2 = 10;
int speedR3 = 11;
int speedL1 = 5;
int speedL2 = 6;
int speedL3 = 7;

int stepTime = 200;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize pins as outputs and initialize direction bits
  pinMode(stepR, OUTPUT);  
  pinMode(dirR, OUTPUT);  
  digitalWrite(dirR, LOW); // shorter
  pinMode(stepL, OUTPUT);  
  pinMode(dirL, OUTPUT);  
  digitalWrite(dirL, LOW); // shorter
  
  // set speed to 16th steps
  pinMode(speedR1, OUTPUT);
  digitalWrite(speedR1, HIGH);  
  pinMode(speedR2, OUTPUT);
  digitalWrite(speedR2, HIGH);  
  pinMode(speedR3, OUTPUT);
  digitalWrite(speedR3, HIGH);
  pinMode(speedL1, OUTPUT);
  digitalWrite(speedL1, HIGH);  
  pinMode(speedL2, OUTPUT);
  digitalWrite(speedL2, HIGH);  
  pinMode(speedL3, OUTPUT);
  digitalWrite(speedL3, HIGH);
}

// Main loop
void loop() {
  digitalWrite(stepR, HIGH);
  digitalWrite(stepL, HIGH);
  delayMicroseconds(10);  
  digitalWrite(stepR, LOW);
  digitalWrite(stepL, LOW);
  delayMicroseconds(stepTime);
  //digitalWrite(stepR, HIGH);
  digitalWrite(stepL, HIGH);
  delayMicroseconds(10);  
  //digitalWrite(stepR, LOW);
  digitalWrite(stepL, LOW);
}
