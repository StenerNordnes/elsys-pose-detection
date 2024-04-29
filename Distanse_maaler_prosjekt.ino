int dl = 50;
int it = 0;
int tid= 3;
int waitIt = tid / (dl*0.001); 
int trigPin = 17;
int echoPin = 16; 
int outPin = 23;
int failSafe = 0;
int failTime = 0.65;
int failit = failTime / (dl*0.001);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(outPin, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) /29.1;
  
  
  if(distance>150 || distance<50){
    digitalWrite(outPin, LOW);
    ++failSafe;
    if(failSafe > failit){ 
      it = 0;
    }
  } 
  else{
    ++it;
    failSafe = 0;
    
}
if(it >= waitIt){
  digitalWrite(outPin, HIGH);
}
  Serial.println("Outpin: ");
  Serial.println(digitalRead(outPin));
  Serial.println("Avstand:  ");
  Serial.println(distance);
  //Serial.println("It: "); 
  //Serial.println(it);  
  delay(dl);
}
