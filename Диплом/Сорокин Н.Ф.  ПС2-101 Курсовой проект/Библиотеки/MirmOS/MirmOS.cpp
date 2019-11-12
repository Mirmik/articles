#include "MirmOS.h"
#include "Arduino.h"
#ifdef INFO_ERROR2
PROGMEM prog_char strDOWN[]="SYSTEM DOWN\n";
PROGMEM prog_char strERR[]="error";
#endif //INFO_ERROR2
#ifdef INFO_ERROR
PROGMEM prog_char endPROG[]=":PROGeNDeRROR\n";
PROGMEM prog_char taskOVF[]=":TASKoVFeRROR\n";
PROGMEM prog_char timOVF[]=":TIMERoVFeRROR\n";
PROGMEM prog_char unkSTR[]=":UNKNOWeRROR\n";
PROGMEM prog_char FSerr[]=":FSerrEND\n";
#endif //INFO_ERROR

extern ring_buffer tx_buffer;

uint8_t FS_numprocess=0;

void (*zeroFunc)(void) =0;

void systemError(uint8_t code)
{

FS_work=0;
#ifdef INFO_ERROR2
Serial.write("\n\n");
systemPrint(strERR,NUMSTREAM);
Serial.print(code,DEC);
#endif //INFO_ERROR2
#ifdef INFO_ERROR
switch (code) {
case 100:systemPrint(endPROG);break;
case 223:systemPrint(timOVF);break;
case 222:systemPrint(taskOVF);break;
case 203:systemPrint(FSerr);break;
default :systemPrint(unkSTR);break;
}
#endif //INFO_ERROR
#ifdef COLLAPSE_ON_SYS_ERROR
#ifdef INFO_ERROR2
systemPrint(strDOWN);
#endif
while(tx_buffer.head!=tx_buffer.tail);
#endif //COLLAPSE_ON_SYS_ERROR
while(1);
}
