#include "Arduino.h"
#include "MirmOS.h"

uint8_t FS_work;
uint8_t FS_numstream=0;
SPstore_t SPstore [SPSIZE];
int a,b;
int u=0;


#ifdef FS
void FS_begin()
{FS_work=1;}

void FS_stop()
{FS_work=0;}

void FS_init()
{for (int i=0;i<SPSIZE;i++) 
SPstore[i].SP_p.i=0;
__malloc_heap_end=(char*)(RAMEND);}

void programm1();

void createStream (void (*stream) (void))
{int temp;
int newstrm;
for (newstrm=0;(newstrm<SPSIZE) && (SPstore[newstrm].SP_p.i!=0);newstrm++); //ищем свободный стек.

newstrm=1;


if (newstrm==SPSIZE) systemError(202);	//Обработка ошибки переполнения.
temp = (int)malloc(STACKDEPTH);	//Выделение памяти под стек.
if (temp==0) systemError(201);	//Обработка ошибки.
SPstore[newstrm].SP_p.i=temp+STACKDEPTH-1;	// Вычисление адреса стека.
SPstore[newstrm].StartSP=SPstore[newstrm].SP_p.i;	// Вычисление адреса стека.
//CLICOPYSREG();

if (FS_numstream==0) writeContext(&(SPstore[newstrm].SP_p.i),RAMEND); //вызов ветвителя из 0-вого потока.
else writeContext(&(SPstore[newstrm].SP_p.i),SPstore[FS_numstream].StartSP);


//RESTORESREG();

// Вызов ветвителя из ненулевого потока.

//В эту точку возвращаются новые потоки. 
//векторы выхода потоков из ветвителя:
if (u==1) {
PORTB=0xFF;
//programm1();
while(1);}

loadStackPointer(SPstore[newstrm]);
loadContext();
asm("reti");


systemError(203);
};


int Taskcount=0;

#endif
	

