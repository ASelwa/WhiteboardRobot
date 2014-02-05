
int stepR = 13;
int dirR = 12;

int speedR1 = 9;
int speedR2 = 10;
int speedR3 = 11;

int stepTime = 900;
int counter = 0;
int toggle = 1;


// the setup routine runs once when you press reset:
void setup() {                
  // initialize pins
  pinMode(stepR, OUTPUT);  
  pinMode(dirR, OUTPUT);  
  digitalWrite(dirR, LOW);
  
  pinMode(speedR1, OUTPUT);
  digitalWrite(speedR1, HIGH);  
  pinMode(speedR2, OUTPUT);
  digitalWrite(speedR2, HIGH);  
  pinMode(speedR3, OUTPUT);
  digitalWrite(speedR3, HIGH);
  
}

// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(stepR, HIGH);
  delayMicroseconds(stepTime);  
  digitalWrite(stepR, LOW);
  delayMicroseconds(stepTime);
}
