#include <Arduino.h>
#include "MirmOS.h"
//#include "PARAMETR.h"
// Определения системных строк выводов.
#ifdef INFO_WELCOME
PROGMEM prog_char WELCOMESTR[]="Arduino MirmOS was included.\n";
PROGMEM prog_char VERSION[]="OS Version 0.1\n";
#endif

void programm();

// MAIN FUNCTION!!!
int main (void)__attribute__((__noreturn__));
int main(void)                      //Точка входа программы.
{
	init();							//Инициализация ядра Ардуино.
Serial.begin(9600);
#ifdef INFO_WELCOME
systemPrint(WELCOMESTR);
systemPrint(VERSION);
#endif
	setup();
	programm();
	systemError(100); 
}

#ifdef FS
//ISR(TIMER2_OVF_vect,ISR_NAKED)
ISR(TIMER2_OVF_vect,ISR_NAKED)
{
if (FS_work==1)
{
saveContext();				// Сохраняем контекст.
	copyStackPointer(SPstore[FS_numstream]);
	FS_numstream++;
	if (FS_numstream==SPSIZE) FS_numstream=0;
  loadStackPointer(SPstore[FS_numstream]);
loadContext();	
asm("reti");				//Возврат из прерывания.
}
}
#endif