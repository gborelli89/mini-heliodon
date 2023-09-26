#include <AccelStepper.h>
#include <MultiStepper.h>

#define HALFSTEP 8

// Define some steppers and the pins the will use
AccelStepper stepperAltitude(HALFSTEP, 4,5,6,7);
AccelStepper stepperAzimuth(HALFSTEP, 8,9,10,11);

MultiStepper steppers;

void setup()
{  
    Serial.begin(9600);
    
    stepperAltitude.setMaxSpeed(300.0);
    stepperAzimuth.setMaxSpeed(300.0);

    steppers.addStepper(stepperAltitude);
    steppers.addStepper(stepperAzimuth);

    //Serial.print("Ready");
    //Serial.print("\n\n");

}

void loop()
{
    String msg_status = "NA";
    String v1 = "NA";
    String v2 = "NA";
    String dt = "NA"; 
    int stepper_status = 0;
    
    long positions[2];

    Serial.write(stepper_status);

    if(Serial.available()){

        String msg_status = Serial.readStringUntil(';');
        String v1 = Serial.readStringUntil(';');
        String v2 = Serial.readStringUntil(';');
        String dt = Serial.readStringUntil('\n');
        
        int valueAlt = v1.toInt();
        int valueAz = v2.toInt();
        int timeinterval = dt.toInt();

        if(msg_status=="movesun"){
          positions[0] = valueAlt;
          positions[1] = valueAz;
          //Serial.print("Moving system...");
          //Serial.print("\n");
          //Serial.print("Altitude value: ");
          //Serial.print(v1);
          //Serial.print("\n");
          //Serial.print("Azimuth value: ");
          //Serial.print(v2);
          //Serial.print("\n\n");
  
          stepper_status = 1;
          Serial.write(stepper_status);
          delay(100);
          
          
          steppers.moveTo(positions);
          steppers.runSpeedToPosition();
        
          if(stepperAzimuth.distanceToGo() < 5){
            delay(timeinterval);
            //stepper_status = 0;
            //Serial.write(stepper_status);
            //Serial.print("Ready");
            //Serial.print("\n\n");
            //delay(500);
          }
    
        }
    }

     delay(100);

}
