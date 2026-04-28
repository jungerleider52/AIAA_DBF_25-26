#include <AccelStepper.h>

// Define stepper driver type (1 = driver with STEP+DIR)
#define MOTOR_INTERFACE_TYPE 1

// Pin definitions
#define A1x 1
#define A2x 2
#define B1x 3
#define B2x 4
#define A1y 5
#define A2y 6
#define B1y 7
#define B2y 8

// Create stepper objects
// below format works for TB6612 (Bipolar, constant voltage, H-Bridge motor driver)
AccelStepper stepperX(AccelStepper::FULL4WIRE, A1x, A2x, B1x, B2x);
AccelStepper stepperY(AccelStepper::FULL4WIRE, A1y, A2y, B1y, B2y);

// Motion settings
float maxSpeed = 800.0;
float acceleration = 400.0;

// Example airfoil path (simple shape for demo)
const int numPoints = 6;
float path[numPoints][2] = {
  {0, 0},
  {50, 10},
  {100, 0},
  {100, -10},
  {50, -5},
  {0, 0}
};

// Conversion factor: mm → steps
float stepsPerMM = 80.0;

// Track current target
int currentPoint = 0;

void setup() {
  Serial.begin(115200);

  stepperX.setMaxSpeed(maxSpeed);
  stepperX.setAcceleration(acceleration);

  stepperY.setMaxSpeed(maxSpeed);
  stepperY.setAcceleration(acceleration);

  Serial.println("Hot Wire Cutter Ready");
}

void loop() {
  if (currentPoint < numPoints) {
    moveToPoint(path[currentPoint][0], path[currentPoint][1]);
    currentPoint++;
    delay(200); // small pause between moves
  }
}

// Function to move both axes together
void moveToPoint(float x_mm, float y_mm) {
  long x_steps = x_mm * stepsPerMM;
  long y_steps = y_mm * stepsPerMM;

  stepperX.moveTo(x_steps);
  stepperY.moveTo(y_steps);

  while (stepperX.distanceToGo() != 0 || stepperY.distanceToGo() != 0) {
    stepperX.run();
    stepperY.run();
  }

  Serial.print("Moved to: ");
  Serial.print(x_mm);
  Serial.print(", ");
  Serial.println(y_mm);
}