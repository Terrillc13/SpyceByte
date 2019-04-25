#include <Arduino.h>
#include "BasicStepperDriver.h"
#include <SharpDistSensor.h>

// Constants for the sensor measurements
#define MEASUREMENTS_DELAY 2 // In milliseconds
#define MEASUREMENTS_TAKEN 100

//Constants for the stepper motors
#define MOTOR_STEPS 200
#define RPM 120
#define MICROSTEPS 16
#define DISPENCE_DELAY 250
#define DIR_1 10
#define STEP_1 2
#define DIR_2 11
#define STEP_2 3
#define DIR_3 12
#define STEP_3 4

// Analog pin to which the sensor is connected
const byte jarSensorPin1 = A0;
const byte jarSensorPin2 = A2;
const byte jarSensorPin3 = A4;

// Window size of the median filter (odd number, 1 = no filtering)
const byte medianFilterWindowSize = 5;


// Create objects for each sensor.
SharpDistSensor sensor1(jarSensorPin1, medianFilterWindowSize);
SharpDistSensor sensor2(jarSensorPin2, medianFilterWindowSize);
SharpDistSensor sensor3(jarSensorPin3, medianFilterWindowSize);

// Create objects for each stepper motor.
BasicStepperDriver stepper1(MOTOR_STEPS, DIR_1, STEP_1);
BasicStepperDriver stepper2(MOTOR_STEPS, DIR_2, STEP_2);
BasicStepperDriver stepper3(MOTOR_STEPS, DIR_3, STEP_3);

/*
   Setup the three stepper motors
   used for dispensing and the
   three sensors used to getFullness.
   Start the serial communication
   for receiving instructions.
*/
void setup() {
  // Setup Dispensors
  stepper1.begin(RPM, MICROSTEPS);
  stepper2.begin(RPM, MICROSTEPS);
  stepper3.begin(RPM, MICROSTEPS);
  // Setup sensor model
  sensor1.setModel(SharpDistSensor::GP2Y0A51SK0F_5V_DS);
  sensor2.setModel(SharpDistSensor::GP2Y0A51SK0F_5V_DS);
  sensor3.setModel(SharpDistSensor::GP2Y0A51SK0F_5V_DS);
  // Begin serial reading
  Serial.begin(9600);
}

/*
   Continuously loop waiting for
   an instuction set to be sent.
   Once an instruction set is
   received via the serial
   communication, perform the
   corresponding action.

   'd' = doDispense
   's' = getFullness (Sensor)

   Format:
   {instruction}{jar}{Optional:Amount}
   doDispense Example: "d112"
      Instruction: doDispense
      Jar: 1
      Amount: 12
   getFullness Example: "s2"
      Instruction: getFullness
      Jar: 2
*/
void loop() {
  // Declare Variables
  String command = "";
  String instruction = "";
  int jar = 0;
  int amount = 0;
  // Wait for the instruction set to come
  if (Serial.available()) {
    command = Serial.readString();
    instruction = command.substring(0, 1);
    jar = command.substring(1, 2).toInt();
    Serial.flush();
  }
  // Dispense using the stepper motors.
  if (instruction == "d") {
    amount = command.substring(2).toInt();
    doDispense(jar, amount);
  }
  // Get the fullness using the sensors.
  else if (instruction == "s") {
    getFullness(jar);
  }
}

/*
   Turn the stepper motor specified
   a certain amount of times.

   int jar - The jar to dispense from.
   int jar - The amount of times the
             stepper motor will rotate
             in half rotation increments.
*/
void doDispense(int jar, int amount) {
  BasicStepperDriver stepper = stepper1;
  if (jar == 2) {
    stepper = stepper2;
  }
  else if (jar == 3) {
    stepper = stepper3;
  }
  for (int i = 0; i < amount; i++) {
    stepper.rotate(180);
    delay(DISPENCE_DELAY);
  }
  Serial.println("Dispense Done");
}

/*
   Calculate the Fullness and send it
   via the serial connection.

   int jar - The jar to get the fullness of.
*/
void getFullness(int jar) {
  // Total will be divided by measurements used.
  double total = 0;
  int measurementsUsed = 0;
  float measurementValueUsed = 0;
  // Measurements taken will be stored in an array.
  unsigned int measurements[MEASUREMENTS_TAKEN];
  // Determine which sensor to use. Use sensor 1 by default.
  SharpDistSensor sensor = sensor1;
  if (jar == 2) {
    sensor = sensor2;
  }
  else if (jar == 3) {
    sensor = sensor3;
  }
  unsigned int measurement = 0;
  // Take the measurements with short delays. Store in array.
  while (measurementsUsed < MEASUREMENTS_TAKEN) {
    // Get distance from sensor and store in array.
    measurement = sensor.getDist();
    //Serial.println(measurement);
    if (measurement > 14 && measurement < 200) {
      measurements[measurementsUsed] = measurement;
      measurementsUsed = measurementsUsed + 1;
      //Serial.println(measurement);
    }
    // Wait some time before taking another measurement.
    delay(MEASUREMENTS_DELAY);
  }
  if (measurementsUsed != 0) {
    //Serial.println("Filter:");
    // Reset counter
    measurementsUsed = 0;
    // Get the average and standard deviation.
    float average = getAverage(measurements, MEASUREMENTS_TAKEN);
    float std = getStdDev(measurements, MEASUREMENTS_TAKEN, average);
    // Only use values that full within twice the standard deviation.
    for (int i = 0; i < MEASUREMENTS_TAKEN; i++) {
      // Get distance from sensor
      if (measurements[i] >= average - std/2 and measurements[i] <= average + std/2) {
        total = total + measurements[i];
        //Serial.println(measurements[i]);
        measurementsUsed = measurementsUsed + 1;
      }
    }
    // Determine a value to use
    if (measurementsUsed > 0) {
      measurementValueUsed = total / measurementsUsed;
    } else {
      // Just in case zero measurements are used.
      measurementValueUsed = average;
    }
  } else {
    measurementValueUsed = 0;
  }
  //Serial.print("Value: ");
  //Serial.println(measurementValueUsed);
  // Convert to fullness percentage
  int fullness = 0;
  if (measurementValueUsed > 50) 
  {
    // The voltage has not been supplied
    fullness = 150-(3.3333*measurementValueUsed);
  }
  else
  {
    // The voltage has been supplied
    fullness = 124-(1.1905*measurementValueUsed);
  }
  // Print the fullness reading to serial.
  if (fullness > 100) {
    Serial.println(100);
  } else if (fullness <0) {
    Serial.println(0);
  } else {
    Serial.println(fullness);
  }
}

/*
   Get the mean from an array of unsigned ints.

   int * val - the array to get the average of.
   arrayCount - the amount of ints in the array.
*/
float getAverage(int * val, int arrayCount) {
  long total = 0;
  for (int i = 0; i < arrayCount; i++) {
    total = total + val[i];
  }
  float avg = total / (float)arrayCount;
  return avg;
}

/*
   Get the standard deviation from an array of unsigned ints.

   int * val - the array to get the average of.
   arrayCount - the amount of ints in the array.
*/
float getStdDev(int * val, int arrayCount, float average) {
  long total = 0;
  for (int i = 0; i < arrayCount; i++) {
    total = total + (val[i] - average) * (val[i] - average);
  }
  float variance = total / (float)arrayCount;
  float stdDev = sqrt(variance);
  return stdDev;
}
