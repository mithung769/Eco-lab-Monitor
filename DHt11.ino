#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
#define LDR_PIN 3
#define RELAY_PIN 7

DHT dht(DHTPIN, DHTTYPE);

const bool RELAY_ACTIVE_LOW = true;

bool relayState = false;  // Controlled ONLY via UI (Python → Serial)

void setRelay(bool on) {
  relayState = on;

  if (RELAY_ACTIVE_LOW) {
    digitalWrite(RELAY_PIN, on ? LOW : HIGH);
  } else {
    digitalWrite(RELAY_PIN, on ? HIGH : LOW);
  }
}

void handleSerialCommand() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();

    if (cmd == "RELAY_ON") {
      setRelay(true);
    } 
    else if (cmd == "RELAY_OFF") {
      setRelay(false);
    }
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(LDR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);

  setRelay(false);

  dht.begin();
  delay(2000);
}

void loop() {

  handleSerialCommand();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  int lightState = digitalRead(LDR_PIN);

  bool isDark = (lightState == HIGH);

  if (isnan(temperature)) temperature = -1;
  if (isnan(humidity)) humidity = -1;

  float voltage = 230.0;
  float current = 0.2;  // assumed
  float power = relayState ? (voltage * current) : 0.0;

  Serial.print("{");
  Serial.print("\"temperature\":");
  Serial.print(temperature, 2);
  Serial.print(",\"humidity\":");
  Serial.print(humidity, 2);
  Serial.print(",\"light\":");
  Serial.print(lightState);
  Serial.print(",\"is_dark\":");
  Serial.print(isDark ? 1 : 0);
  Serial.print(",\"relay\":");
  Serial.print(relayState ? 1 : 0);
  Serial.print(",\"power\":");
  Serial.print(power, 2);
  Serial.println("}");

  delay(2000);
}