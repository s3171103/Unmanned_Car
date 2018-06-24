String msg="";
int a;
String commande = "hhhh";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
   while(Serial.available() > 0){
       a=Serial.read();
       Serial.println(a);
       //if (a==10) break;
   }
   //Serial.println(a);
  // put your main code here, to run repeatedly:
  //Serial.println(commande);
  //commande = Serial.readString();
  delay(800);
}

