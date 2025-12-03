float posX, posY;
float velX, velY;

const float WORLD_WIDTH = 800.0;
const float WORLD_HEIGHT = 600.0;
const float RADIUS = 15.0;
const float GRAVITY_Y = 0.0; 
const float PANTULAN = -0.7; 
const float DORONGAN = 200.0; 
const float DAMPING_FACTOR = 1.0; 

unsigned long lastTimeMicros = 0;
float dt = 0.0;

unsigned long lastPrintTime = 0;
const long PRINT_INTERVAL = 30; 

void setup() {
  Serial.begin(115200);

  posX = WORLD_WIDTH / 2.0;
  posY = WORLD_HEIGHT / 2.0;
  velX = 0.0;
  velY = 0.0;
  
  lastTimeMicros = micros();
  lastPrintTime = millis();
}

void loop() {
  unsigned long nowMicros = micros();
  dt = (nowMicros - lastTimeMicros) / 1000000.0; 
  lastTimeMicros = nowMicros;
  if (dt > 0.1) { dt = 0.1; }
  if (dt <= 0.0) { dt = 0.0001; }

  if (Serial.available() > 0) {
    char inputChar = Serial.read();
    while(Serial.available() > 0) { Serial.read(); }

    if (inputChar == 'w' || inputChar == 'W') { velY = -DORONGAN; }
    if (inputChar == 's' || inputChar == 'S') { velY = DORONGAN; }
    if (inputChar == 'a' || inputChar == 'A') { velX = -DORONGAN; }
    if (inputChar == 'd' || inputChar == 'D') { velX = DORONGAN; }
  }

  velY += GRAVITY_Y * dt;
  
  float damping_multiplier = 1.0 - (DAMPING_FACTOR * dt);
  if (damping_multiplier < 0.0) { damping_multiplier = 0.0; } 
  
  velX *= damping_multiplier;
  velY *= damping_multiplier; 

  posX += velX * dt;
  posY += velY * dt;

  if (posY + RADIUS > WORLD_HEIGHT) { posY = WORLD_HEIGHT - RADIUS; velY *= PANTULAN; }
  if (posY - RADIUS < 0) { posY = RADIUS; velY *= PANTULAN; }
  if (posX + RADIUS > WORLD_WIDTH) { posX = WORLD_WIDTH - RADIUS; velX *= PANTULAN; }
  if (posX - RADIUS < 0) { posX = RADIUS; velX *= PANTULAN; }

  unsigned long nowMillis = millis();
  if (nowMillis - lastPrintTime > PRINT_INTERVAL) {
    lastPrintTime = nowMillis;    

    Serial.print(posX); Serial.print(",");
    Serial.print(posY); Serial.print(",");
    Serial.print(velX); Serial.print(",");
    Serial.print(velY); Serial.print(",");
    Serial.println(dt, 6); 
  }
}