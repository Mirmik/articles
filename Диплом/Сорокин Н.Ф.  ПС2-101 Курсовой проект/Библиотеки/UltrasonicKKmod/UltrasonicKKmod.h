/*
  Ultrasonic.h - Library for HR-SC04 Ultrasonic Ranging Module.
  Created by ITead studio. Alex, Apr 20, 2010.
  iteadstudio.com
  
  updated by noonv. Feb, 2011
  http://robocraft.ru
*/

#ifndef Ultrasonic_h
#define Ultrasonic_h

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif 

#define DUR 2
#define CM 1
#define INC 0

class Ultrasonic
{
  public:
    Ultrasonic(int TP, int EP);
    void Timing();
	void Duration (int);
    long Ranging();
	unsigned int starttimer;
 long  duration,distacne_cm,distance_inc;
    
    private:
    int Trig_pin;
    int Echo_pin;
   
};

#endif //#ifndef Ultrasonic_h
