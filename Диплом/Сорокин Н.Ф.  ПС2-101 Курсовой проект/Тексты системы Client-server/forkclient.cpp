
#include <sys/types.h>
 #include <unistd.h>
 #include <stdlib.h>
 #include <stdio.h>

 int main()
 {

     if (fork() == 0) {
                 execl("/root/client","/root/client", (char *) 0);
         perror("exec one failed");
        exit(1);
        
     }
      exit(0);
  }
