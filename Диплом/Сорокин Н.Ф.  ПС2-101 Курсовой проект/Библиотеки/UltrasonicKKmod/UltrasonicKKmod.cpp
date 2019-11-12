/*
  Ultrasonic.cpp - Library for HC-SR04 Ultrasonic Ranging Module.library

  Created by ITead studio. Apr 20, 2010.
  iteadstudio.com
  
  updated by noonv. Feb, 2011
  http://robocraft.ru
*/

#include "UltrasonicKKmod.h"

Ultrasonic::Ultrasonic(int TP, int EP)
{
   pinMode(TP, OUTPUT);
   pinMode(EP, INPUT);
   Trig_pin=TP;
   Echo_pin=EP;
}


volatile long timer1_cicles=0;
long sonar_timer_cicles=0;

ISR(TIMER1_OVF_vect)
{timer1_cicles++;}

void Ultrasonic::Timing()
{
 digitalWrite(Trig_pin, LOW);
 delayMicroseconds(1);
 digitalWrite(Trig_pin, HIGH);
delayMicroseconds(5);
  digitalWrite(Trig_pin, LOW);
cli();
  starttimer=(unsigned int)TCNT1;
sonar_timer_cicles=timer1_cicles;
sei();
   return;
}

long Ultrasonic::Ranging()
{
 return  duration;
}

void Ultrasonic::Duration(int dur)
{cli();
duration=dur+(timer1_cicles-sonar_timer_cicles)*63556;sei();
}