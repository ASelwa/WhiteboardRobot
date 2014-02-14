#include <stdio.h> // for function sprintf

int pin_stepR = 13;
int pin_dirR = 12;
int pin_stepL = 1;
int pin_dirL = 0;

int pin_speedR1 = 9;
int pin_speedR2 = 10;
int pin_speedR3 = 11;
int pin_speedL1 = 5;
int pin_speedL2 = 6;
int pin_speedL3 = 7;

int BASE_FREQ = 5000; // Hz

// the setup routine runs once when you press reset:
void setup() {                
  // initialize pins as outputs and initialize direction bits
  pinMode(pin_stepL, OUTPUT);  
  pinMode(pin_dirL, OUTPUT);
  pinMode(pin_stepR, OUTPUT);
  pinMode(pin_dirR, OUTPUT);     
  digitalWrite(pin_dirL, LOW); // Shorter
  digitalWrite(pin_dirR, LOW); // shorter
  
  // set speed to 16th steps
  pinMode(pin_speedR1, OUTPUT);
  pinMode(pin_speedR2, OUTPUT);
  pinMode(pin_speedR3, OUTPUT);
  
  pinMode(pin_speedL1, OUTPUT);
  pinMode(pin_speedL2, OUTPUT);
  pinMode(pin_speedL3, OUTPUT);
  
  digitalWrite(pin_speedR1, LOW); 
  digitalWrite(pin_speedR2, HIGH);  
  digitalWrite(pin_speedR3, LOW);
  
  digitalWrite(pin_speedL1, LOW);  
  digitalWrite(pin_speedL2, HIGH);  
  digitalWrite(pin_speedL3, LOW);
  
  // For serial printing (debugging)
  //Serial.begin(9600);
  
  
}

// the loop routine runs over and over again forever:
void loop() {
  //Serial.println("Start");
  //Serial.println(micros());
  segment(5000, 10000, BASE_FREQ);
  //Serial.println(micros());
  //Serial.println("After function called");
  //unsigned long x = micros();
  //double y = 0.9;
  //String xStr;
  //sprintf(xStr, "%d", x);
  //Serial.println(x);
  //Serial.println(x+y);
  delay(10000);
  //digitalWrite(stepR, HIGH);
  //digitalWrite(stepL, HIGH);
  //delayMicroseconds(10);  
  //digitalWrite(stepR, LOW);
  //digitalWrite(stepL, LOW);
  //delayMicroseconds(stepTime);
}






void segment(long stepL, long stepR, int BASE_FREQ) {
  // Function that moves the motors for one segment
  
  unsigned long dTimeL = 2000;
  unsigned long dTimeR = 2000;
  unsigned long stepsDoneL = 0;
  unsigned long stepsDoneR = 0;
  
  
  
  // Take the larger step count and assign BASE_FREQ
  // Adjust so the frequencies allow for the motors to reach the destination at the same time.  
  // 1000000 multiplied to get a delta t in microseconds
  if (stepL > stepR) {
    dTimeL = 1000000/BASE_FREQ;
    //dTimeR = (stepL*1000000)/(stepR*BASE_FREQ);
    dTimeR = 1000000/BASE_FREQ;
    dTimeR = dTimeR*(stepL/stepR);
  }
  else {
    dTimeR = 1000000/BASE_FREQ;
    dTimeL = 1000000/BASE_FREQ;
    dTimeL = dTimeL*(stepR/stepL);
  }
  
  // Start the marked times for each of the motors
  unsigned long markedTimeL = micros();
  unsigned long markedTimeR = micros();
    
  
  // Loop and keep stepping until the proper number of steps has been done
  while ((stepsDoneL <= stepL) && (stepsDoneR <= stepR))  {  
     
    // LEFT MOTOR
    unsigned long testTime = micros();
    if (testTime > markedTimeL+dTimeL) {
      // Step the motor
      digitalWrite(pin_stepL, HIGH);
      delayMicroseconds(20);  
      digitalWrite(pin_stepL, LOW); 
      
      // Increase steps done and reset the time placeholder for the left motor
      stepsDoneL = stepsDoneL + 1;  
      markedTimeL = micros();
      }
     
     // RIGHT MOTOR
     if (micros() > markedTimeR+dTimeR) {
       // Step the motor
      digitalWrite(pin_stepR, HIGH);
      delayMicroseconds(20);  
      digitalWrite(pin_stepR, LOW); 
      
      // Increase steps done and reset the time placeholder for the right motor
      stepsDoneR = stepsDoneR + 1; 
      markedTimeR = micros();      
     }
  } 
}
