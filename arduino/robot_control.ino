#include <Servo.h>
#define HEAD_SERVO_PIN 9
#define BODY_SERVO_PIN 10

#define SERVO_MOVE_DELAY_TIME 30

#define HEAD_CONTROL_POT_PIN A5
#define BODY_CONTROL_POT_PIN A4
#define HEAD_POT_PIN A2
#define BODY_POT_PIN A1

#define LED_PIN 6

Servo head_servo;
Servo body_servo;

void manual_control(){
  int deg_head = map(analogRead(HEAD_CONTROL_POT_PIN), 0,1024,50,130);
  Serial.print(deg_head);
  Serial.print(" : ");
  Serial.print(map(analogRead(HEAD_POT_PIN),400,700,0,255));
  Serial.print(" << HEAD ");
  head_servo.write(deg_head);
  
  int deg_body = map(analogRead(BODY_CONTROL_POT_PIN), 0,1024,50,130);
  Serial.print(deg_body);
  Serial.print(" : ");
  Serial.print(map(analogRead(BODY_POT_PIN),400,700,0,255));
  Serial.println(" << BODY ");
  body_servo.write(deg_body);
  delay(SERVO_MOVE_DELAY_TIME);
  
}

void setup() {
  head_servo.attach(HEAD_SERVO_PIN);
  body_servo.attach(BODY_SERVO_PIN);
  Serial.begin(9600);
  pinMode(HEAD_CONTROL_POT_PIN, INPUT);
  pinMode(BODY_CONTROL_POT_PIN, INPUT);
  pinMode(HEAD_POT_PIN, INPUT);
  pinMode(BODY_POT_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
}

String num="100\n";

void loop() {
  if (Serial.available()){
//    int num  = Serial.read()-'0';
    num = Serial.readString();
    Serial.println(num);
  }

  if (num.equals("100\n")){
     manual_control();
     digitalWrite(LED_PIN, HIGH);
  }else
  {
     digitalWrite(LED_PIN, LOW);
  }
}
