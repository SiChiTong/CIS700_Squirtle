double raw_input = 0; 
double offset = 512;
double static this_output = 0;
double static last_output = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
  Serial.begin(115200);
  double sum = 0;
  for (int i=0; i<10000; i++ ){
    sum += analogRead(A0);
    delay(0.1);
  }
  offset = sum/10000.0;
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);

}

void loop() {
  
  raw_input = analogRead(A0)-offset;
  if(raw_input<0)raw_input = -raw_input;
  
  this_output = 0.1 * raw_input + 0.9 * last_output;
  Serial.println(this_output);
  last_output = this_output;

}
