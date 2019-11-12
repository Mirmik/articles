#include "MirmForceSH_assemf.h"
#include <avr/io.h>

.global copyContext
.global writeContext


copyContext:         ;метка входа в функцию.
mov r26,r24          ;int SPstore..i addr
mov r27,r25          ;
mov r28,r22			 ;int start
mov r29,r23

ld r30,X+            ;Загрузка SPstore..i
ld r31,X+

lds r24,SPL
lds r25,SPH

adiw r24,2

adiw r28,1				; Инкрементация (математика)  
adiw r30,1           ;Инкрементация регистровой пары Z
                     ;нужна по соображениям хитрой 
					 ;адресной математики 
					 ;С инициализацией закончили.

copyContext_1:		 ;Точка входа рабочего цикла


LD r20,-Y            ;Декрементировать Y, после чего (r28,r29)
					 ;ЗАГРУЗИТЬ В регистр r20
					 ;содержимое ИЗ ячейки на которую Y
					 ;ссылается
					  	 
ST -Z,r20            ;Декрементировать Z, после чего (r30,r31)
					 ;ЗАПИСАТЬ ИЗ регистра r20 
					 ;содержимое В ячейку на которую Z
					 ;ссылается
					  
cp r24,r28		  
brne copyContext_1   
cp r25,r29
brne copyContext_1   

;ldi r31,1
;ldi r30,0

st -X,r31
st -X,r30
ret            ;Деректива возврата из функции 


dela:
ldi r16,255
ldi r17,255
ldi r18,20
dela1:
dec r16
brne dela1
dec r17
brne dela1
dec r18
brne dela1
ret

debug:
cre:
nop
rjmp cre
ret





writeContext:         ;метка входа в функцию.
mov r26,r24          ;int SPstore..i addr
mov r27,r25          ;

ld r30,X+            ;Загрузка SPstore..i
ld r31,X+

mov r26,r22
mov r27,r23

lds r18,SPL
lds r19,SPH

adiw r26,1
adiw r30,1            

copyContext_2:		 ;Точка входа рабочего цикла


LD r20,-X            ;Декрементировать X, после чего (r26,r27)
					 ;ЗАГРУЗИТЬ В регистр r20
					 ;содержимое ИЗ ячейки на которую Y
					 ;ссылается
					  	 
ST -Z,r20            ;Декрементировать Z, после чего (r30,r31)
					 ;ЗАПИСАТЬ ИЗ регистра r20 
					 ;содержимое В ячейку на которую Z
					 ;ссылается
					  
cp r18,r26		  
brne copyContext_2   
cp r19,r27
brne copyContext_2   



ST -Z,r0
in r18, sreg
ST -Z,r18
ST -Z,r1
ST -Z,r2
ST -Z,r3
ST -Z,r4
ST -Z,r5
ST -Z,r6
ST -Z,r7
ST -Z,r8
ST -Z,r9
ST -Z,r10
ST -Z,r11
ST -Z,r12
ST -Z,r13
ST -Z,r14
ST -Z,r15
ST -Z,r16
ST -Z,r17
ST -Z,r18
ST -Z,r19
ST -Z,r20
ST -Z,r21
ST -Z,r22
ST -Z,r23
ST -Z,r24
ST -Z,r25
ST -Z,r26
ST -Z,r27
ST -Z,r28
ST -Z,r29
ST -Z,r30
ST -Z,r31


mov r26,r24
mov r27,r25

ST X+,r30
ST X+,r31
ret            ;Деректива возврата из функции 