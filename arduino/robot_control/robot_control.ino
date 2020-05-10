#include <Servo.h>
#define HEAD_SERVO_PIN 9
#define BODY_SERVO_PIN 10

#define SERVO_MOVE_DELAY_TIME 30

#define HEAD_CONTROL_POT_PIN A5
#define BODY_CONTROL_POT_PIN A4
#define HEAD_POT_PIN A2
#define BODY_POT_PIN A1

#define LED_PIN 6

#define MIN_SERVO_DEG  30
#define MAX_SERVO_DEG  130

Servo head_servo;
Servo body_servo;
int msg[4];

void setup() {
  head_servo.attach(HEAD_SERVO_PIN);
  body_servo.attach(BODY_SERVO_PIN);
  pinMode(HEAD_CONTROL_POT_PIN, INPUT);
  pinMode(BODY_CONTROL_POT_PIN, INPUT);
  pinMode(HEAD_POT_PIN, INPUT);
  pinMode(BODY_POT_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  exec_command(80, 90); // center robot
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
  
  for (int i = 0 ; i<3; i++){
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
   }

  Serial.println("1000");
}

void show_pot_data(){
  Serial.println(map(analogRead(HEAD_POT_PIN),300,700,0,255));
  Serial.println(map(analogRead(BODY_POT_PIN),300,700,0,255));
}


void manual_control(int deg_head, int deg_body){
  /* Control the robot with pots and display servo degree rotations*/
  head_servo.write(deg_head);
  body_servo.write(deg_body);
  
  delay(SERVO_MOVE_DELAY_TIME);
  
}

void exec_command(int deg_head, int deg_body){

  if ((deg_head <= MAX_SERVO_DEG && deg_head >= MIN_SERVO_DEG) &&
      (deg_body <= MAX_SERVO_DEG && deg_body >= MIN_SERVO_DEG)){
         
      manual_control(deg_head, deg_body);
        
  }
}

void loop() {
  if(Serial.available()){
    for(int i=0; i<4 ;i++){
        msg[i] = Serial.read();
        Serial.flush();
      }
     
  }

  if (msg[0]==100){
    digitalWrite(LED_PIN, HIGH);
    int deg_head = map(analogRead(HEAD_CONTROL_POT_PIN), 0,1024, MIN_SERVO_DEG, MAX_SERVO_DEG);
    int deg_body = map(analogRead(BODY_CONTROL_POT_PIN), 0,1024, MIN_SERVO_DEG, MAX_SERVO_DEG);
    manual_control(deg_head, deg_body);
  }else if (msg[0]==101){
    digitalWrite(LED_PIN, LOW);
    exec_command(msg[1], msg[2]);
  }

//  if (msg[3] == 100){
    show_pot_data();
//  }
}
