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

void setup() {
  head_servo.attach(HEAD_SERVO_PIN);
  body_servo.attach(BODY_SERVO_PIN);
  pinMode(HEAD_CONTROL_POT_PIN, INPUT);
  pinMode(BODY_CONTROL_POT_PIN, INPUT);
  pinMode(HEAD_POT_PIN, INPUT);
  pinMode(BODY_POT_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  exec_command("080090"); // center robot
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
  Serial.print(map(analogRead(HEAD_POT_PIN),300,700,0,255));
  Serial.print(":");
  Serial.println(map(analogRead(BODY_POT_PIN),300,700,0,255));
}


void manual_control(int deg_head, int deg_body, bool show_log){
  /* Control the robot with pots and display servo degree rotations*/
  head_servo.write(deg_head);
  body_servo.write(deg_body);
  
//  if (show_log){
//    Serial.print(deg_head);
//    Serial.print(" << HEAD ");
//    Serial.print(deg_body);
//    Serial.println(" << BODY ");
//  }
  
  delay(SERVO_MOVE_DELAY_TIME);
  
}

void exec_command(String num){
  /* takes string composed of 6 numbers eg.'080090' . 
     first 3 numbers '080' describe head position in degrees for servo and last
     3 are for body.
     if numbers are less than 100 they must contain 0 in front of them to enable 
     correct parsing.   
  */
  if (!num.equals("101\n") && !num.equals("101\n")){
    int deg_head = (num.substring(0,3)).toInt();
    int deg_body = (num.substring(3,6)).toInt();
  // Serial.println(deg_head);
    if ((deg_head <= MAX_SERVO_DEG && deg_head >= MIN_SERVO_DEG) &&
        (deg_body <= MAX_SERVO_DEG && deg_body >= MIN_SERVO_DEG)){
          
          manual_control(deg_head, deg_body, false);
        
        }
    
//    Serial.println(map(analogRead(HEAD_POT_PIN),300,700,0,255));
//    Serial.println(map(analogRead(BODY_POT_PIN),300,700,0,255));
   }
}

String num = "";
int option=2;

void loop() {
  if (Serial.available()){
//    int num  = Serial.read()-'0';
    num = Serial.readString();
//    delay(10);
//    Serial.println(num);
    if (num.equals("100\n")){
      Serial.println(num);
      option = 0;
      digitalWrite(LED_PIN, HIGH);
    }else if (num.equals("101\n")){
      Serial.println(num);
      option = 1;
      digitalWrite(LED_PIN, LOW);
    }else if (num.equals("102\n")){
      show_pot_data();
    }

    if (option==1){
      exec_command(num);
    }
  }

  if (option==0){ // manual control no continous serial com. is necessary
    int deg_head = map(analogRead(HEAD_CONTROL_POT_PIN), 0,1024, MIN_SERVO_DEG, MAX_SERVO_DEG);
    int deg_body = map(analogRead(BODY_CONTROL_POT_PIN), 0,1024, MIN_SERVO_DEG, MAX_SERVO_DEG);
    manual_control(deg_head, deg_body, true);  
  }  

  
//    Serial.print(analogRead(HEAD_POT_PIN));
//    Serial.print(" ");
//    Serial.println(analogRead(BODY_POT_PIN));
}
