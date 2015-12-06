double raw_input_1 = 0; 
double offset_1 = 512;
double static this_output_1 = 0;
double static last_output_1 = 0;

double raw_input_2 = 0; 
double offset_2 = 512;
double static this_output_2 = 0;
double static last_output_2 = 0;


void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
  Serial.begin(115200);
  double sum = 0;
  for (int i=0; i<10000; i++ ){
    sum += analogRead(A0);
    delay(0.1);
  }
  offset_1 = sum/10000.0;
  
  sum = 0;
  for (int i=0; i<10000; i++ ){
    sum += analogRead(A1);
    delay(0.1);
  }
  offset_2 = sum/10000.0;
  
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);

}

void loop() {

  raw_input_1 = analogRead(A0)-offset_1;
  if(raw_input_1<0)raw_input_1 = -raw_input_1;
  
  this_output_1 = 0.1 * raw_input_1 + 0.9 * last_output_1;
  Serial.println(this_output_1);
  last_output_1 = this_output_1;

  raw_input_2 = analogRead(A1)-offset_2;
  if(raw_input_2<0)raw_input_2 = -raw_input_2;
  
  this_output_2 = 0.1 * raw_input_2 + 0.9 * last_output_2;
  Serial.println(this_output_2);
  last_output_2 = this_output_2;  
  

}
