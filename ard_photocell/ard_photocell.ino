// PhotoCell
const int photoR = A0; // Photoresistor at Arduino analog pin A0
int sensorValue = 0;  // ADC: Photoresistor (0-1023)

// General Variable
const int baud_rate = 9600;
const int sampletime = 100; //loop cycle 10ms
String stringsum;

// Arduino initial Set-up
void setup() {
  Serial.begin(baud_rate);
}

// Arduino loop
void loop() {
  // Sensor Read & Get data
  sensorValue = analogRead(photoR);
  // Serial.println(sensorValue);
  
  // separate multi-datas to string: 'ia' data-1 'b' data-2 'f'
  stringsum = "ia" + String(sampletime) + "b" + String(sensorValue) + "f";
  Serial.println(stringsum);
  
  while (millis() % sampletime != 0);
}