
#ifndef Mirm_OS_h
#define Mirm_OS_h

#include "Arduino.h"
#include "PARAMETR1.h"  
#include "MirmOS_FS.h"
#include "MirmOS_INFO.h"
#include "MirmOS_CS.h"
#include "MirmForceSH_assemf.h"
#include <avr/pgmspace.h>

#define CLICOPYSREG() uint8_t global_temp=SREG;cli();
#define RESTORESREG() SREG=global_temp;
#define NUMSTREAM 1



// Глобальные переменные ОС
extern uint8_t global_temp;
extern uint8_t FS_work;
extern uint8_t FS_numstream;
extern SPstore_t SPstore [SPSIZE];

void systemError(uint8_t code);


void memTest(char *x,char *y);

#endif

