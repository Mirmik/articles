#define KK

#include "MirmOS.h"
#include "UltrasonicKKmod.h"
#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz,gy2;

#define startKvat 0x0FFF

long l0=startKvat,l1=0,l2=0,l3=0;
long l0n,l1n,l2n,l3n;

unsigned int temp[4];
char servN,servNflag;

unsigned int serv[4];

#define ALTITUDE 230
#define TIMCORRECT 2000

#define MOTOR1 5
#define MOTOR2 6
#define MOTOR3 7
#define MOTOR4 8

long intax,intaz,intdist,intgy,intgx,intgz;
int servsumm,servsumm2;
int servdiff_y=0,servdiff_x=0,servcomp_z=0;
int startgx,startgy,startgz,startaz,startax,startay;
long intphi_x,intphi_y,intphi_z;
#define Kax 0.0005*4



int dist=0,edist;
int intazop=14500;


coopShedulerType SH;
long req;
#define TIMESTOP 20000
#define STARTMINUS 250*16
#define Kc 1.4
#define Kd 1.00
#define TKK 0.5

// sensor connected to:
// Trig - 2, Echo - 3
Ultrasonic ultrasonic(2, 3);

int flag=0;

void startdur()
{int dur=(unsigned long)TCNT1 - (unsigned long)ultrasonic.starttimer;
if (!(dur<5000)) ultrasonic.Duration(dur);
}

// Мигание светодиодом
void t1(){PORTB=PORTB|(1<<6);if (flag==1) SH.newTask(t2,100*TKK);}
void t2(){PORTB=PORTB&(~(1<<6));SH.newTask(t1,100*TKK);}


void setup() {
TCCR1A=(0<<COM1A1) | (0<<COM1A0) | (0<<COM1B1) | (0<<COM1B0) | (0<<WGM11) | (0<<WGM10);
TCCR1B=(0<<ICNC1) | (0<<ICES1) | (0<<WGM13) | (0<<WGM12) | (0<<CS12) | (0<<CS11) | (1<<CS10);
TIMSK1=1;

	Wire.begin();
    accelgyro.initialize();
	Serial.begin(38400);
	attachInterrupt(1, startdur, HIGH);
   //Serial.write(accelgyro.testConnection() ? "MPU6050 connection successful\n" : "MPU6050 connection failed\n");
}
void programm()
{
servsumm=0;
SH.start(idle,intask);
	
}

long timerestart;
char flag_restart_gyr=1;

void restart()
{timerestart=millis();
PORTB=PORTB&(~(1<<6));
delay(200);
PORTB=PORTB|(1<<6);
SH.newTask(gyrostart);
flag_restart_gyr=1;
}

char data;
char strrest[]="gyrcorrect";
char strdvstart[]="startdv";
char strdvstop[]="stop";
char nchargyr=0;
char ncharstart=0;
char ncharstop=0;

void idle()
{
	if (Serial.available()) {data=Serial.read();
	if (data == strrest[nchargyr]) {nchargyr++;}
	else {nchargyr=0;}
	if (data == strdvstart[ncharstart]) {ncharstart++;}
	else {ncharstart=0;}
	if (data == strdvstop[ncharstop]) {ncharstop++;}
	else {ncharstop=0;}
	if (nchargyr==10) SH.newTask(restart);
	if (ncharstart==7) SH.newTask(startdv);
	if (ncharstop==4) SH.newTask(stoptask2);
	}
}

void startdv ()
{
intdist=0;
edist=0;
intaz=0;
flag=1;
t1();
SH.newTask(task1);
req=millis();
SH.newTask(stoptask,TIMESTOP);
}

void intask() 
{
SH.newTask(restart);
SH.newTask(taskPrint);
SH.newTask(sonar);
}


// Функции остановки двигателе
void stoptask2()
{flag=0;}
void stoptask()
{if ((millis()-req)>TIMESTOP-1000) flag=0;}


void sonar()
{ ultrasonic.Timing(); 	
	edist=150;
	intdist=intdist+edist;
    SH.newTask(sonar,10);
}

int servnum[4];
int tempserv;
char tempnum;
unsigned int s[4];


ISR(TIMER1_COMPA_vect)
{	TIMSK1=0;
	digitalWrite(servN+5,0);
	servN++;
	if (servN!=4) SH.newTask(impulse);
}

// Подача серво импульса на движки. Работает в комбинации с прерыванием ISR(TIMER1_COMPA_vect)
void impulse (void)
{
	digitalWrite(servN+5,1);

OCR1A=TCNT1+serv[servN];
TIFR1=TIFR1 |(1<<OCF1A);                                        // Очистка флага прерывания.
TIMSK1=(0<<ICIE1) | (0<<OCIE1B) | (1<<OCIE1A) | (0<<TOIE1);
}


#define K_idist (0.02*3.86*0.05)*16
#define K_pdist (0.01*3.86)*16
#define K_iaz (-2*0.001)*16

#define Kf 0.2

#define K_y			0.05 *0.6*4
#define Kp_y		(K_y				 /8           *3       )     
#define Ki_y		(K_y *0.002        *1000 *0.45	*	1.8	)
#define Kintphi_y	(K_y*0.000004	   *1000  *1.2 *5 /2/2  	)

#define K_x			K_y
#define Kp_x		Kp_y
#define Ki_x		Ki_y      
#define Kintphi_x	Kintphi_y       

#define K_z			(0.00960      *2)
#define Kp_z		(K_z		         *3 *1.2     )
#define Ki_z		(K_z	*0.002       *3 *0.45 *5    *1000 )
#define Kintphi_z	(K_z*0.000004     *1.6 *1000   )

#define Kax 0.0003 *16


//#define LIMITSERV 100
#define LIMITSERV 100*16
#define LIMITDIFF 100*16   //otmena
//130 - polet 2 motora 1047



// Гироскоп. Исходная, начальная, текущая информация. Время коррекции (TIMCORRECT) определено в define.
int br=1;
int k=1;
int n=0;
void gyrostart()
{PORTB=PORTB|(1<<6);
flag=0;
accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
intgx=0;
intgy=0;
intgz=0;
intaz=0;
intphi_x=-70/Kintphi_x;
intphi_y=-0/Kintphi_y;
intphi_z=-150/Kintphi_z;

n=0;
SH.newTask(gyrcorrect,100);
}
void gyrcorrect()
{accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
intgx=intgx+gx;
intgy=intgy+gy;
intgz=intgz+gz;
intaz=intaz+az;
n++;
if (millis()-timerestart<TIMCORRECT) SH.newTask(gyrcorrect,1);
else{
startgx=intgx/n;
startgy=intgy/n;
startgz=intgz/n;
startaz=intaz/n;
l0=startKvat;
l1=0;
l2=0;
l3=0;
intgx=0;intgy=0;intgz=0;intaz=0;
SH.newTask(kvaternion);
flag_restart_gyr=0;}
}

long w1;long w2; long w3;
double filtrgx,filtrgy,filtrgz,filtraz;
#define Kvatnorm 1/21278/2    *10 //?
#define h 0.002

long z;
double norm;
void kvaternion()
{accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

filtraz=az-(az-filtraz)*0.75;
filtrgx=gx-(gx-filtrgx)*Kf;
filtrgy=gy-(gy-filtrgy)*Kf;
filtrgz=gz-(gz-filtrgz)*Kf;


az=filtraz;
gx=filtrgx;
gy=filtrgy;
gz=filtrgz;

	w1=gx-startgx;w2=gy-startgy;w3=gz-startgz;

l0n=l0+(-l1*w1-l2*w2-l3*w3)*Kvatnorm*h;
l1n=l1+( l0*w1-l3*w2+l2*w3)*Kvatnorm*h;
l2n=l2+( l3*w1+l0*w2-l1*w3)*Kvatnorm*h;
l3n=l3+(-l2*w1+l1*w2+l0*w3)*Kvatnorm*h;

norm=sqrt(l0n*l0n+l1n*l1n+l2n*l2n+l3n*l3n)/startKvat;

l0=l0n/norm;
l1=l1n/norm;
l2=l2n/norm;
l3=l3n/norm;

intaz=intaz*0.975+(az-startaz);
//z=z+intaz;

intgx=l1;
intphi_x=intphi_x+intgx;

intgy=l2;
intphi_y=intphi_y+intgy;

intgz=l3;
intphi_z=intphi_z+intgz;

if (!flag_restart_gyr) SH.newTask(kvaternion,2);
}


#define Ki_az 0.003

void task1()
{  
servdiff_y=-(gy-startgy)*Kp_y -intgy*Ki_y -intphi_y*Kintphi_y;
servdiff_x=-(gx-startgx)*Kp_x -intgx*Ki_x -intphi_x*Kintphi_x;

servcomp_z= - Kp_z*(gz-startgz) - Ki_z * intgz -intphi_z*Kintphi_z;




if (servdiff_y>LIMITDIFF) servdiff_y=LIMITDIFF;
if (servdiff_y<-LIMITDIFF) servdiff_y=-LIMITDIFF;
if (servdiff_x>LIMITDIFF) servdiff_x=LIMITDIFF;
if (servdiff_x<-LIMITDIFF) servdiff_x=-LIMITDIFF;
if (servcomp_z>LIMITDIFF) servcomp_z=LIMITDIFF;
if (servcomp_z<-LIMITDIFF) servcomp_z=-LIMITDIFF;


servsumm2=intdist*K_idist+edist*K_pdist;

if (servsumm2>LIMITSERV+STARTMINUS) servsumm2=LIMITSERV+STARTMINUS ;

servsumm=servsumm2-(intaz)*Ki_az - (az-startaz)/36000 *0;

if (ultrasonic.duration <8000) servsumm=servsumm-(8000-ultrasonic.duration); 

serv[0] =  10000*1.14+(servsumm+servdiff_y-STARTMINUS+servcomp_z)*Kc;
serv[1] =  10000     +(servsumm-servdiff_y-STARTMINUS+servcomp_z)   ;
serv[2] =  10000     +(servsumm-servdiff_x-STARTMINUS-servcomp_z)   ;
serv[3] =  10000     +(servsumm+servdiff_x-STARTMINUS-servcomp_z)   ;

	
servN=0;
SH.newTask(impulse);

if (flag==1) SH.newTask(task1,10);
}
  
void taskPrint()
{
Serial.print(intgx*Ki_x); Serial.write("\t");
Serial.print(intgy*Ki_y); Serial.write("\t");
Serial.print(intgz*Ki_z); Serial.write("\t\t");
Serial.print(intphi_x*Kintphi_x); Serial.write("\t");
Serial.print(intphi_y*Kintphi_y); Serial.write("\t");
Serial.print(intphi_z*Kintphi_z); Serial.write("\t\t");
Serial.print(intaz*Ki_az); Serial.write("\t\t");
Serial.print(servsumm); Serial.write("\t\n ");

SH.newTask(taskPrint,20);
}

