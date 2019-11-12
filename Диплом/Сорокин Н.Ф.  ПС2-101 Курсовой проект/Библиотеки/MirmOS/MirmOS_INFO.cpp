//#include "MirmOS.h"
#include "MirmOS_INFO.h"


extern ring_buffer tx_buffer;



char buffer[BUFFERSIZE];



void systemPrint(prog_char str[],uint8_t numstream)
{
uint8_t localTemp=SREG;cli();uint8_t printTemp=FS_work;FS_work=0;sei();
if (numstream!=0) {Serial.write(FS_numstream);Serial.write(":");}
strcpy_P(buffer, str); 
Serial.write( buffer );
while(tx_buffer.head!=tx_buffer.tail);FS_work=printTemp;SREG=localTemp;
}
