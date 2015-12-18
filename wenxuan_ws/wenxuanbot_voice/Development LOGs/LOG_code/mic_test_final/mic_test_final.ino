
double offset_mic_x; 
double offset_mic_y;
double offset_mic_z;


////////////PORT Specify////////////////////////
#define PORT_MIC_X A0   // indicate which AD port you connect
#define PORT_MIC_Y A1
#define PORT_MIC_Z A2



///////////Parameter Setup/////////////////////
long const BAUD_RATE = 230400;  //Serial Baud Rate
float const FILTER_THIS = 0.1;  //Low-pass Filter Param
float const FILTER_LAST = 0.9;  //Low-pass Filter Param


//////////////////////////////////////////////

void setup() {
  
  Serial.begin(BAUD_RATE);

  offset_mic_x = auto_offset_compute(PORT_MIC_X);
  offset_mic_y = auto_offset_compute(PORT_MIC_Y);
  offset_mic_z = auto_offset_compute(PORT_MIC_Z); 
  
  led_blink();
  
}

void loop() {

  get_mic_strength("mic_x");
  get_mic_strength("mic_y");
  get_mic_strength("mic_z");

}

double get_mic_strength(String mic){
// this function is for getting microphone strength value
// which is basically a filtered absolute microphone altitude
// argument can be "mic_x" "mic_y" or "mic_z"
  int raw_input = 0;
  
  if (mic.equals("mic_x")){
    
      raw_input = analogRead(PORT_MIC_X)-offset_mic_x;
      if(raw_input < 0) raw_input = -raw_input;

      double static this_output_x;
      double static last_output_x;
      this_output_x = FILTER_THIS * raw_input + FILTER_LAST * last_output_x;
      Serial.println(this_output_x);
      last_output_x = this_output_x;   
      return this_output_x;
      
  }else if (mic.equals("mic_y")){
    
      raw_input = analogRead(PORT_MIC_Y)-offset_mic_y;
      if(raw_input < 0) raw_input = -raw_input;
 
      double static this_output_y;
      double static last_output_y;
      this_output_y = FILTER_THIS * raw_input + FILTER_LAST * last_output_y;
      Serial.println(this_output_y);
      last_output_y = this_output_y; 
      return this_output_y;
        
  }else if (mic.equals("mic_z")){
    
      raw_input = analogRead(PORT_MIC_Z)-offset_mic_z;
      if(raw_input < 0) raw_input = -raw_input;
 
      double static this_output_z;
      double static last_output_z;
      this_output_z = FILTER_THIS * raw_input + FILTER_LAST * last_output_z;
      Serial.println(this_output_z);
      last_output_z = this_output_z;   
      return this_output_z;
  }
  
  return 0.0; //indicating failure
  
}

double auto_offset_compute(int port){
  // this is for computing zero offset of a particular AD port
  // takes argument A0~A5, returns offset 
  double sum = 0;
  for (int i=0; i<10000; i++ ){
    sum += analogRead(port);
    delay(0.1);
  }
  return sum/10000.0;
}

void led_blink(){
  pinMode(13,OUTPUT);
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);
  digitalWrite(13,HIGH);delay(500);
  digitalWrite(13,LOW);delay(500);  
}

