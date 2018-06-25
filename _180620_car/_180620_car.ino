/*     Arduino Rotary Encoder Tutorial
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */
 float timeF_R,timeF_L,sp;
 float time0_R,time0_L = 0.0;
 #define LOOPTIME        100 
unsigned long lastMilli = 0;                    // loop timing 
unsigned long lastMilliPrint = 0;   
float speed_act_R = 0;
float speed_act_L = 0; 
int speed_req_R = 300; 
int PWM_val_R = 0; 
int speed_req_L = 300; 
int PWM_val_L = 0; 
float Kp =   .4;                                // PID proportional control Gain
float Kd =    1;  

const byte IN1 = 6;   // 馬達B 的正反轉接腳編號
const byte IN2 = 5;
const byte ENA = 7;   // 馬達B 的 P

const byte IN3 = 8;   // 馬達B 的正反轉接腳編號
const byte IN4 = 9;
const byte ENB = 10;   // 馬達B 的 PWM 轉速控制
int speed;      // 定義速度變數，PWM 輸出範圍為 0～255
 
 #define outputA 11
 #define outputB 12
 #define outputA 2
 #define outputB 3
 int counter_L = 0; 
 int counter_R = 0;
 int aState_R,aState_L;
 int aLastState_R,aLastState_L;  
 void setup() { 
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
 
  speed = 100; //初始化速度
  
   pinMode (outputA,INPUT);
   pinMode (outputB,INPUT);
   
   Serial.begin (115200);
   // Reads the initial state of the outputA
   aLastState_R = digitalRead(outputA);   
   aLastState_L = digitalRead(outputB);   
 } 
 
 void printMotorInfo()  {                                                      // display data
 if((millis()-lastMilliPrint) >= 500)   {                     
   lastMilliPrint = millis();
   Serial.print("SP_R:");             Serial.print(speed_act_R);  
   Serial.print("  SP_L:");      Serial.print(speed_req_L);
   Serial.print("  outputA:");      Serial.println(digitalRead(outputA));  
 }
}

void getMotorData()  {                                                        // calculate speed, volts and Amps
static long countAnt_R = 0;                                                   // last count
static long countAnt_L = 0;   
 speed_act_R = ((counter_R - countAnt_R)*(60*(1000/LOOPTIME)))/(16*29);          // 16 pulses X 29 gear ratio = 464 counts per output shaft rev
 countAnt_R = counter_R;                  
 speed_act_L = ((counter_L - countAnt_L)*(60*(1000/LOOPTIME)))/(16*29);          // 16 pulses X 29 gear ratio = 464 counts per output shaft rev
 countAnt_L = counter_L;
}

int getParam2(){
  String speed_tmp ;
  speed_tmp="";
  char s ;
  while(Serial.available()>0){
    s = Serial.read();
    if (s != '\n'){
      speed_tmp += s;
    }
  }
  Serial.println(speed_tmp);
}

int getParam()  {
char param, cmd;
 if(!Serial.available())    return 0;
 delay(10);                  
 param = Serial.read();                              // get parameter byte
 if(!Serial.available())    return 0;
 cmd = Serial.read();                                // get command byte
 Serial.flush();
 switch (param) {
   case 'v':                                         // adjust speed
     if(cmd=='+')  {
       speed_req_R += 20;
       speed_req_L += 20;
       if(speed_req_R>400)   speed_req_R=400;
       if(speed_req_L>400)   speed_req_L=400;
     }
     if(cmd=='-')    {
       speed_req_R -= 20;
       speed_req_L -= 20;
       if(speed_req_R<0)   speed_req_R=0;
       if(speed_req_L<0)   speed_req_L=0;
     }
     break;
   case 's':                                        // adjust direction
     if(cmd=='+'){
       digitalWrite(IN1, LOW);
       digitalWrite(IN2, HIGH);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, HIGH);
     }
     if(cmd=='-')   {
       digitalWrite(IN1, HIGH);
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, HIGH);
       digitalWrite(IN4, LOW);
     }
     break;
   case 'o':                                        // user should type "oo"
     digitalWrite(IN1, LOW);
     digitalWrite(IN2, LOW);
     digitalWrite(IN3, LOW);
     digitalWrite(IN4, LOW);
     speed_req_R = 0;
     speed_req_L = 0;
     break;
   default: 
     Serial.println("???");
   }
}

int updatePid(int command, int targetValue, int currentValue)   {             // compute PWM value
float pidTerm = 0;                                                            // PID correction
int error=0;                                  
static int last_error=0;                             
 error = abs(targetValue) - abs(currentValue); 
 pidTerm = (Kp * error) + (Kd * (error - last_error));                            
 last_error = error;
 return constrain(command + int(pidTerm), 0, 255);
}

 void loop() { 
 getParam2(); 
 if((millis()-lastMilli) >= LOOPTIME)   {                                    // enter tmed loop
   lastMilli = millis();
   printMotorInfo();
   getMotorData();                                                           // calculate speed, volts and Amps
   PWM_val_R= updatePid(PWM_val_R, speed_req_R, speed_act_R);                        // compute PWM value
   PWM_val_L= updatePid(PWM_val_L, speed_req_L, speed_act_L);
 }
 
  analogWrite(ENA, PWM_val_R);
  analogWrite(ENB, PWM_val_L);

   aState_R = digitalRead(outputA); // Reads the "current" state of the outputA
   // If the previous and the current state of the outputA are different, that means a Pulse has occured
   if (aState_R != aLastState_R){   
     timeF_R = millis();
     sp = (timeF_R-time0_R)*100;
     // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
     if (digitalRead(outputA) != aState_R) { 
       counter_R ++;
     } else {
       counter_R --;
     }
     time0_R = millis();
   } 
   aLastState_R = aState_R; // Updates the previous state of the outputA with the current state
 

    aState_L = digitalRead(outputB); // Reads the "current" state of the outputA
   // If the previous and the current state of the outputA are different, that means a Pulse has occured
   if (aState_L != aLastState_L){   
     timeF_L = millis();
     sp = (timeF_L-time0_L)*100;
     // If the outputB state is different to the outputA state, that means the encoder is rotating clockwise
     if (digitalRead(outputB) != aState_L) { 
       counter_L ++;
     } else {
       counter_L --;
     }
     time0_L = millis();
   } 
   aLastState_L = aState_L; // Updates the previous state of the outputA with the current state
  }

