#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "stdio.h"
#include <unistd.h>
#include <arpa/inet.h>

char str[4]="aba";

int main()
{
    int sock, listener;
    struct sockaddr_in addr;
    char buf[1024];
    int bytes_read;

    listener = socket(AF_INET, SOCK_DGRAM, 0);
    if(listener < 0)
    {
        perror("socket");
        return 1;
    }
    
    addr.sin_family = AF_INET;
    addr.sin_port = htons(10666);
    addr.sin_addr.s_addr = inet_addr("192.168.1.38");
    if(bind(listener, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        perror("bind");
        return 2;
    }

  //  listen(listener, 1);
    
/*        sock = accept(listener, NULL, NULL);
        
        if(sock < 0)
        {
            perror("accept");
            return 3;
        }*/
sock=listener;
        while(1)
			{
            bytes_read = recv(sock, buf, 1024, 0);
            if(bytes_read <= 0) break;
            //send(sock, buf, bytes_read, 0);
           write(0, buf, bytes_read);
        }
    
        close(sock);
    
    return 0;
}
