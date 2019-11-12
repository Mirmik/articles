
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
  
char symb=0;
int z;
char indata[200];
char str[] ="\nЕсть Cвязь\n";
char pass[4];

int main()
{
	// Инициализация Клиента
    int sock,listener;
    struct sockaddr_in addr;
//	unsigned int client_addr_size=sizeof(addr);
    listener = socket(AF_INET, SOCK_STREAM, 0);
    if(listener < 0)
    {
        perror("socket");
        return 1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(10670); // или любой другой порт...
    addr.sin_addr.s_addr = inet_addr("192.168.1.120");
    
    // END. Инициализация Клиента
   /* if(bind(listener, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind");
        return 2;
    }*/
    sock=listener;
//listen(listener, 0x100);
while(connect(sock, (struct sockaddr *)&addr, sizeof(addr)));
       
       
write(0,str,20);   
 
while(1){   
	z=read(0,indata,200);
	strncpy(pass,indata,4);
	if (strcmp(pass,"exit")==0) { close(sock); close(listener); return 0;}
send(sock,indata,z,0);

}
 
    close(sock);

    return 0;
}
