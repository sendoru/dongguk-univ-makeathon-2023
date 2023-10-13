// Additional board manage blah
// https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json

#include <DynamixelWorkbench.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_NeoPixel.h>

#if defined(__OPENCM904__)
  #define DEVICE_NAME "3" //Dynamixel on Serial3(USART3)  <-OpenCM 485EXP
#elif defined(__OPENCR__)
  #define DEVICE_NAME ""
#endif   

#define BAUDRATE  1000000
#define DXL_ID    1
#define PIN_IN    5
#define PIN_OUT   6
#define PIN_5V_0  8

DynamixelWorkbench dxl_wb;
LiquidCrystal_I2C lcd(0x27, 16, 2);
Adafruit_NeoPixel neoPixel(4, 3);

int last_status = LOW, curr_status = LOW;

// debounce funtion that prevents input jittering
bool debounce(bool last_status, uint32_t pin) {
  bool curr_status = digitalRead(pin);
  if (last_status != curr_status) {
    delay(5);
    curr_status = digitalRead(pin);
  }
  return curr_status;
}

void callback() {
  Serial.println("Dynamixel is moving...");

  // Turn on flashlight
  neoPixel.setPixelColor(1, 200, 200, 200);
  neoPixel.show();
  delay(50);

  for (int count = 0; count < 6; count++) {
    // rotate motor
    Serial.println("Rotating...");
    dxl_wb.goalPosition(DXL_ID, count * 1024 / 6);

    // send electric signal to RPi via digitalWrite
    // so that RPi captures image
    delay(500);
    digitalWrite(PIN_OUT, HIGH);
    delay(250);
    digitalWrite(PIN_OUT, LOW);
  }

  // Turn off flashlight
  neoPixel.setPixelColor(0, 0, 0, 0);
  neoPixel.show();

  // Reset motor position
  dxl_wb.goalPosition(DXL_ID, 0);
  Serial.println("Return from callback function");
}

void setup() 
{
  lcd.init();
  lcd.backlight();

  neoPixel.begin();
  neoPixel.show();

  Serial.begin(57600);
  // while(!Serial); // Wait for Opening Serial Monitor

  const char *log;
  bool result = false;

  uint8_t dxl_id = DXL_ID;
  uint16_t model_number = 0;

  pinMode(PIN_IN, INPUT);
  pinMode(PIN_OUT, OUTPUT);
  pinMode(PIN_5V_0, OUTPUT);
  digitalWrite(PIN_5V_0, HIGH);

  result = dxl_wb.init(DEVICE_NAME, BAUDRATE, &log);
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to init dynamixel:");
  }
  else {
    Serial.print("Succeeded to init dynamixel:");
  }

  result = dxl_wb.ping(DXL_ID, &model_number, &log);
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else {
    Serial.println("Succeeded to ping");
  }

  result = dxl_wb.jointMode(DXL_ID, 0, 0, &log);
  if (result == false) {
    Serial.println(log);
    Serial.println("Failed to change joint mode");
  }
  else {
    Serial.println("Succeed to change joint mode");
  }

  dxl_wb.goalPosition(DXL_ID, 1000);

  delay(1000);
  dxl_wb.goalPosition(DXL_ID, 0);

  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
  lcd.display();
}

void loop()  {
  while (Serial.available() == 0) {
    curr_status = debounce(last_status, PIN_IN);
    if (last_status == LOW && curr_status == HIGH) {
      callback();
    }
    last_status = curr_status;
    Serial.println(curr_status);
  }

  // TODO readString 이거 어떻게 쓰는거지
  // This get IP address and port no. from RPi via Serial comm.
  String str = Serial.readStringUntil('\n');
  str.trim();
  if (str != "") {
    Serial.println("Received IP address and port no. from RPi");
    lcd.setCursor(0, 0);
    lcd.print(str);
  }
}