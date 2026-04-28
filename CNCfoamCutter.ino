#include <Stepper.h>

const int STEPS = 200;   // steps per revolution (adjust for your motor)

// -------------------- StepperMotor Class --------------------
class StepperMotor {
  private:
    Stepper motor;
    int direction = 1;
    int currentPosition = 0;

  public:
    StepperMotor(int steps, int p1, int p2, int p3, int p4)
      : motor(steps, p1, p2, p3, p4) {}

    void setSpeed(int rpm) {
      motor.setSpeed(rpm);
    }

    void setDirection(int d) {
      direction = d;
    }

    void move() {
      motor.step(direction);
      currentPosition += direction;
    }

    int getPosition() {
      return currentPosition;
    }
};

// -------------------- CNC Controller --------------------
struct Instruction {
  int xStep;
  int yTarget;
};

const int MAX_INSTRUCTIONS = 100;
Instruction program[MAX_INSTRUCTIONS];

int programLength = 0;
int instructionIndex = 0;

StepperMotor xMotor(STEPS, 2, 3, 4, 5);
StepperMotor yMotor(STEPS, 6, 7, 8, 9);

int currentStep = 0;
int yTarget = 0;

// -------------------- Setup --------------------
void setup() {
  Serial.begin(9600);

  xMotor.setSpeed(60);
  yMotor.setSpeed(60);

  Serial.println("Send instructions as: xStep,yTarget");
  Serial.println("Example: 100,20");
}

// -------------------- Read Serial Instructions --------------------
void readInstruction() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    int comma = input.indexOf(',');

    if (comma > 0 && programLength < MAX_INSTRUCTIONS) {
      int x = input.substring(0, comma).toInt();
      int y = input.substring(comma + 1).toInt();

      program[programLength].xStep = x;
      program[programLength].yTarget = y;
      programLength++;

      Serial.print("Stored: X=");
      Serial.print(x);
      Serial.print(" Y=");
      Serial.println(y);
    }
  }
}

// -------------------- Smooth Y Movement --------------------
void updateY() {
  if (yMotor.getPosition() != yTarget) {
    int dir = (yTarget > yMotor.getPosition()) ? 1 : -1;
    yMotor.setDirection(dir);
    yMotor.move();
  }
}

// -------------------- Main Loop --------------------
void loop() {
  // Read incoming instructions
  readInstruction();

  // Move X continuously
  xMotor.setDirection(1);
  xMotor.move();
  currentStep++;

  // Check if it's time to update Y target
  if (instructionIndex < programLength &&
      currentStep == program[instructionIndex].xStep) {

    yTarget = program[instructionIndex].yTarget;

    Serial.print("New Y target: ");
    Serial.println(yTarget);

    instructionIndex++;
  }

  // Move Y gradually toward target
  updateY();

  delay(5); // controls overall speed
}