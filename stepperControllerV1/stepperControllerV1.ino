#include <stdio.h> // for function sprintf
#include <math.h>

int pin_stepR = 13;
int pin_dirR = 12;
int pin_stepL = 3;
int pin_dirL = 2;

int pin_speedR1 = 9;
int pin_speedR2 = 10;
int pin_speedR3 = 11;
int pin_speedL1 = 5;
int pin_speedL2 = 6;
int pin_speedL3 = 7;

double SPEED = 30; // Desired speed in mm/s
double RADIUS = 13.5; // Estimate of spool radius in mm
double WIDTH = 1530; // Estimate of whiteboard width in mm
double HEIGHT = 1000; // Estimate of whiteboard height in mm
float ANGLE = 1.8*(M_PI/180); // Angle for one full step in rads
float stepFraction;

double curX; // Current location
double curY;

// the setup routine runs once when you press reset:
void setup() {     
  SPEED = SPEED/1000000; // Speed conversion
  // initialize serial:
  Serial.begin(9600);

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
  
  digitalWrite(pin_speedR1, HIGH); 
  digitalWrite(pin_speedR2, HIGH);  
  digitalWrite(pin_speedR3, HIGH);
  
  digitalWrite(pin_speedL1, HIGH);  
  digitalWrite(pin_speedL2, HIGH);  
  digitalWrite(pin_speedL3, HIGH);
  
  stepFraction = 16;
  curX = 600;
  curY = 600;
}

// Main loop
void loop() {
  //segment(WIDTH/2,WIDTH/2,1000,100);
  // Open serial monitor, make sure Newline and 9600 are selected
  // Then send x1,x2,y1,y2
  
  // while there is something in the serial buffer
  while (Serial.available() > 0) {
    // look for the next valid integer in the incoming serial stream, separated by commas
    int x1 = Serial.parseInt(); 
    int x2 = Serial.parseInt(); 
    int y1 = Serial.parseInt(); 
    int y2 = Serial.parseInt();

    // look for the newline. Excecute code
    if (Serial.read() == '\n') {
      longSegment(x1, x2, y1, y2);
      // Update location
      //curX += x2 - x1;
      //curY += y2 - y1;
      
      // Write "a" so that python can wait to send the next line
      //Serial.write("a");
      delay(10); 
    }
  }
}

// Because of non linearity of the lengths l1 and l2, we need to draw short
// lines so they remain locally linear.
// Recursively call lines that are a maximum of 20mm
void longSegment(double x1, double x2, double y1, double y2) {
  double distance = sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
  if (distance > 20) {
    longSegment(x1,(x1+x2)/2,y1,(y1+y2)/2);
    longSegment((x1+x2)/2,x2,(y1+y2)/2,y2);
  }
  else {
    segment(x1,x2,y1,y2);
  }
}
    

// Function that moves the motors for one segment
void segment(double x1, double x2, double y1, double y2) {
  
  // Initialize counter to know when segment is done
  unsigned long stepsDoneL = 0;
  unsigned long stepsDoneR = 0;
  
  // Figure out lengths
  double leftLength1 = sqrt(x1*x1+y1*y1); // in mm
  double leftLength2 = sqrt(x2*x2+y2*y2);
  double rightLength1 = sqrt((WIDTH-x1)*(WIDTH-x1)+y1*y1);
  double rightLength2 = sqrt((WIDTH-x2)*(WIDTH-x2)+y2*y2);
  double deltaLeft = leftLength2 - leftLength1;
  double deltaRight = rightLength2 - rightLength1;
  
  // Set motor speeds (dTime)
  double distance = sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)); // distance of segment in x-y plane
  double time = distance/SPEED; // in us: time it should take each motor to complete the segment
  double speedLeft = fabs(deltaLeft/time); // in mm/us: speed in length of wire
  double speedRight = fabs(deltaRight/time);
  // delay time is (step_angle*radius)/speed
  unsigned long dTimeL = ((ANGLE/stepFraction)*(RADIUS))/speedLeft;
  unsigned long dTimeR = ((ANGLE/stepFraction)*(RADIUS))/speedRight;
  
  // Figure out total number of steps to do so we know when to stop
  unsigned long stepL = fabs(deltaLeft/((ANGLE/stepFraction)*RADIUS));
  unsigned long stepR = fabs(deltaRight/((ANGLE/stepFraction)*RADIUS));
  
  // Set direction bits
  if (deltaLeft < 0) {
    digitalWrite(pin_dirL, LOW); //shorter
  } else {
    digitalWrite(pin_dirL, HIGH); //longer
  }
  if (deltaRight < 0) {
    digitalWrite(pin_dirR, LOW); //shorter
  } else {
    digitalWrite(pin_dirR, HIGH); //longer
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
      stepsDoneL++;
      markedTimeL = micros();
      }
     
     // RIGHT MOTOR
     if (micros() > markedTimeR+dTimeR) {
       // Step the motor
      digitalWrite(pin_stepR, HIGH);
      delayMicroseconds(20);  
      digitalWrite(pin_stepR, LOW); 
      
      // Increase steps done and reset the time placeholder for the right motor
      stepsDoneR++;
      markedTimeR = micros();      
     }
  } 
}
