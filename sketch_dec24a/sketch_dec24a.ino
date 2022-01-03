#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

// Wifi ayarları
#define WIFI_SSID "Anonymous"
#define WIFI_PASSWORD "Makarna52"

// FireBase 
#define API_KEY "AIzaSyBnkuNGPicpGOb4Hv0EaMdtLwKu3FuU6WA"
#define DATABASE_URL "https://iotproje-d97e6-default-rtdb.europe-west1.firebasedatabase.app/" 

FirebaseData firebase;

FirebaseAuth auth;
FirebaseConfig config;

#define LED D1
unsigned long sendDataPrevMillis = 0;
int intValue;
float floatValue;
bool signupOK = false;

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  pinMode(LED, OUTPUT);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Baglandi.");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  /* Assign the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  if (Firebase.ready() && signupOK){
    if (Firebase.RTDB.getInt(&firebase, "/test/LED_STATUS")) {
      intValue = firebase.intData();
      if (intValue == 1) { 
        digitalWrite(LED, HIGH);
      }
      else{
        digitalWrite(LED, LOW);
      }
    }
    else {
      Serial.println(firebase.errorReason());
    }
  }
}
