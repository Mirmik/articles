//#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "stdio.h"
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <string.h> /* String function definitions */
#include <unistd.h> /* UNIX standard function definitions */
#include <fcntl.h> /* File control definitions */
#include <termios.h> /* POSIX terminal control definitions */
#include <pthread.h>
  
char message[] = "Hello there!\n";
char symb=0;
char buf[sizeof(message)];
void * console (void* arg);
struct sockaddr_in addr;
int fd;

int main()
{
int z; 
char indata[2500];

fd = open("/dev/ttyATH0",O_RDWR | O_NOCTTY | O_NDELAY);
if (fd == -1) fd = open("/dev/ttyUSB0",O_RDWR | O_NOCTTY | O_NDELAY);
if (fd == -1)
{ 
printf("open_port: Unable to open ports ");return 0;
}


	// Инициализация Клиента
    int sock;

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock < 0)
    {
        perror("socket");
        return 1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(10666); // или любой другой порт...
    addr.sin_addr.s_addr = inet_addr("192.168.1.35");
    if(connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("connect");
        return 2;
    }
    // END. Инициализация Клиента
    
   // Инициализация Клиента Консоли
    int sock2;
    
    sock2 = socket(AF_INET, SOCK_STREAM, 0);
    if(sock < 0)
    {
        perror("socket");
        return 1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(10670); // или любой другой порт...
   addr.sin_addr.s_addr = inet_addr("192.168.1.120");
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    if(bind(sock2, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
      perror("bind");
        return 2;
    }
       // END. Инициализация Клиента Консоли
   
    pthread_t tid;
	pthread_create(&tid,NULL, console, &sock2);
    
tcflush(fd, TCIFLUSH);
while(1){   
z=read(fd,indata,200);
indata[z]=0;
//write(0,indata,z);
send(sock,indata,z,0);
}
    
    close(sock);

    return 0;
}

void* console (void* sock)
{int bytes_read;
char buf[100];
int sock2=*((int*)sock);
int sock3;
	unsigned int client_addr_size=sizeof(addr);

while(1){
	
listen(sock2, 0x100);
while(1) {
sock3 = accept(sock2, (struct sockaddr *)&addr, &client_addr_size);
           
        if(sock3 < 0)
        {
            perror("accept");
            return 0;
        }
      
	write(0, message, 11);
//while(connect(sock2, (struct sockaddr *)&addr, sizeof(addr)));
    
while(1){
		bytes_read = recv(sock3, buf, 100, 0);
        if(bytes_read <= 0) break;
      //  write(0, buf, bytes_read); 
        write(fd, buf, bytes_read); 
		//write(0, buf, bytes_read);  
}
}} 

close(sock2);		        	
	return 0;}
