#include <ZumoMotors.h>
#include <QTRSensors.h>
unsigned char SENSORS[] = {4, A3, 11, A0, A2, 5};
const int NUM_SENSORS = sizeof(SENSORS);
const int TIMEOUT = 2000;  // waits for 2500 microseconds for sensor outputs to go low
const int EMITTER_PIN = 2;     // emitter is controlled by digital pin 2
const int SENSOR_LEFT_OUTER = 0;
const int SENSOR_RIGHT_OUTER = 5;
 
const int WHITE_THRESH = 700;
const int BLACK_THRESH = 2000;
 
const int SPEED = 50;
ZumoMotors motors;
QTRSensorsRC qtrrc(SENSORS, NUM_SENSORS, TIMEOUT, EMITTER_PIN);
unsigned int sensorValues[NUM_SENSORS];

void spinRight()
{
motors.setSpeeds(SPEED+50,-SPEED-50);
delay(1000);
motors.setSpeeds(0,0);

}
void spinLeft()
{
motors.setSpeeds(-SPEED-50,SPEED+50);
delay(1000);
motors.setSpeeds(0,0);
}
void goForward(int speed1,int time1)
{
   motors.setSpeeds(speed1, speed1);
   delay(abs(time1));
   motors.setSpeeds(0,0);
   delay(10);
}
void setup() {
 Serial.begin(9600);
 //Serial.print("Motors on \n");
 //motors.setSpeeds(SPEED, SPEED);
 //spinLeft();
  
}



void loop() {
  char s1;
  char s2;
  int left = 0;
  int right = 0;
  String s = "";
  // put your main code here, to run repeatedly:
  if (Serial.available()) { 
    s1 = Serial.read();
    while(s1 != 'l'){
      s+=s1;
      s1 = Serial.read();
    }
    left = s.toInt();
    s = "";
    s2 = Serial.read();
    while(s2 != 'r'){
      s+=s2;
      s2 = Serial.read();
    }
    right = s.toInt();
  }
  Serial.println(left);
  Serial.println(right);
  motors.setSpeeds(left,right);
  
  delay(200);
 /*
 if (Serial.available()) {
  String s = "";
  char s1 = Serial.read();
  while(s1 != 'x'){
    s+=s1;
    s1 = Serial.read();
  }
  if(s.toInt() < 0){
    goForward(-SPEED,s.toInt());
  }
  else{
    goForward(SPEED,s.toInt());
  }
  s= "";
  char s2 = Serial.read();
  while(s2 != 'y'){
    s+=s2;
    s2 = Serial.read();
  }
  if(s.toInt() < 0){
    spinLeft();  
  }
  else{
    spinRight();
  }
   goForward(SPEED,s.toInt());
 }
  delay(500);
  */
}

