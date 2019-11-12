#include "Arduino.h"
#include "MirmOS.h"


#ifndef Mirm_OS_INFO
#define Mirm_OS_INFO

#if (RAMEND < 1000)
  #define SERIAL_BUFFER_SIZE 16
#else
  #define SERIAL_BUFFER_SIZE 64
#endif

struct ring_buffer
{
  unsigned char buffer[SERIAL_BUFFER_SIZE];
  volatile unsigned int head;
  volatile unsigned int tail;
};

void systemPrint(prog_char str[],uint8_t numstream=0);


#endif