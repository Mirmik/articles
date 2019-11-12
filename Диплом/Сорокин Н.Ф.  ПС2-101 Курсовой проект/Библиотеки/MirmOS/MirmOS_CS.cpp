#include "MirmOS.h"
#include "Arduino.h"
#include <avr/pgmspace.h>



PROGMEM prog_char SHSTART1[]="StartSH idle=p";
PROGMEM prog_char SHSTART2[]=" init=p";
PROGMEM prog_char SHSTART3[]="\n";
PROGMEM prog_char STOPSTR[]="CoopSH was stoped\n";


long coopShedulerType::noIdleTime(){return (millis()-lastIdleTime);}

void coopShedulerType::start(void (*idle) (void),void (*init) (void))
{
#ifdef CS_INFO
CLICOPYSREG();
systemPrint(SHSTART1,NUMSTREAM);Serial.print((int)idle);systemPrint(SHSTART2);Serial.print((int)init);systemPrint(SHSTART3);
RESTORESREG();
#endif
if ((int)init!=0) newTask(init); 
 {while(1)										
	{unsigned long int m = millis();											
		for (int i=0;i<TimerArrayLength;i++)						
		{if (TimerArray.timerStop[i]!=0)								
			if (m >= TimerArray.timerStop[i])	
			{	newTask(TimerArray.task[i]);						
			TimerArray.timerStop[i]=0;									
			}														
		}															
		if (TCL==TCH) {signal=IDLESIG;lastIdleTime=m;idle();}						
																	
	else																
	{signal=WORKSIG;	
	TCL++;	
	if (TCL>=TaskArrayLength) TCL=0;
	if ((int)TaskArray[TCL]==-1) {
	#ifdef CS_INFO
	systemPrint(STOPSTR,NUMSTREAM);
	#endif
	return;};												
	TaskArray[TCL]();			
	}																														
	}																
}}

void coopShedulerType::stop(void)
{newTask((void(*)())-1);signal=STOPSIG;
}

void coopShedulerType::newTask(void (*task) (void))
{CLICOPYSREG();
TCH++;
if (TCH>=TaskArrayLength) TCH=0;
if (TCL==TCH) { 
systemError(222); 
}
TaskArray[TCH]=task;
RESTORESREG();}


void coopShedulerType::newTask(void (*task) (void),unsigned int timer)
{CLICOPYSREG();
unsigned long int m=millis();
	int k=0;
	for (;((TimerArray.timerStop[k]!=0) && (k!=TimerArrayLength));k++) {} ;	
	if (k==TimerArrayLength) {
	systemError(223);	
	}
	TimerArray.timerStop[k]=timer+m;
	TimerArray.task[k]=task;
RESTORESREG();
	return;
}

coopShedulerType::coopShedulerType()
{TCL=0;
TCH=0;
signal=0;
for (int i=0;i<TimerArrayLength;i++)
{
TimerArray.timerStop[i]=0;
}}