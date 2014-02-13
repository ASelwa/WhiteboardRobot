/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.
 
  This example code is in the public domain.
 */
 
// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int stepLeft = 1;
int stepRight = 13;
int dirLeft = 0;
int dirRight = 12;

int toggle = 1;
int counter = 0;

// the setup routine runs once when you press reset:
void setup() {                
  // initialize the digital pin as an output.
  pinMode(stepRight, OUTPUT);  
  pinMode(dirRight, OUTPUT);  
  pinMode(stepLeft, OUTPUT);  
  pinMode(dirLeft, OUTPUT);  
  digitalWrite(dirLeft, LOW);
  digitalWrite(dirRight, LOW);
      digitalWrite(stepRight, LOW);    // turn the LED off by making the voltage LOW
    digitalWrite(stepLeft, LOW);
}

// the loop routine runs over and over again forever:
void loop() {
  
  /*
  digitalWrite(stepRight, HIGH);   // turn the LED on (HIGH is the voltage level)
    delayMicroseconds(400);               // wait for a second
    counter = counter + 1;
    digitalWrite(stepRight, LOW);    // turn the LED off by making the voltage LOW
    delayMicroseconds(400);  */             // wait for a second
    
  
  // RIGHT MOTOR TESTING
 // for (int i = 1; i < 1500; i++) {
    digitalWrite(stepRight, HIGH);   // turn the LED on (HIGH is the voltage level)
    digitalWrite(stepLeft, HIGH); 
    delayMicroseconds(400);               // wait for a second
    counter = counter + 1;
    digitalWrite(stepRight, LOW);    // turn the LED off by making the voltage LOW
    digitalWrite(stepLeft, LOW);
    delayMicroseconds(400);               // wait for a second
    
    /*if (counter == 1000) {
      counter = 0;
      if (toggle == 1) {
        digitalWrite(dirRight, HIGH);
        toggle = 0;
      }
      else {
        digitalWrite(dirRight, LOW);
        toggle = 1;
      }
    }*/
 //}
  
  
  //counter = 0;
  // LEFT MOTOR TESTING
  /* for (int i = 1; i < 1500; i++) {
    digitalWrite(stepLeft, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(5);               // wait for a second
    counter = counter + 1;
    digitalWrite(stepLeft, LOW);    // turn the LED off by making the voltage LOW
    delay(5);               // wait for a second
    
    if (counter == 500) {
      counter = 0;
      if (toggle == 1) {
        digitalWrite(dirLeft, HIGH);
        toggle = 0;
      }
      else {
        digitalWrite(dirLeft, LOW);
        toggle = 1;
      }
    }
  }*/
  
    
}
