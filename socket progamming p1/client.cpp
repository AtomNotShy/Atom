#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <iostream>
#define MAXIMUM 64
using namespace std;

int main(){
    // create socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));  //fill with 0
    serv_addr.sin_family = AF_INET;  //IPv4
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  //local ip
    serv_addr.sin_port = htons(33147);  //port
    connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
   
    while (1)
    {
        printf("Client is up and running.\n");
        cout<<"Enter City Name:";
        char msg[MAXIMUM]={0};
        cin.getline(msg, MAXIMUM);
        int status = send(sock, msg, MAXIMUM, 0);
        if (status == -1)
        {
            cout<<"error";
            exit(1);
        }
        
        char buffer[64]={0};
        int status1 = recv(sock, buffer, 64, 0);
        if (status1 <= 0)
        {
            cout<<"error";
            exit(1);
        }

        string state;
        for (int i = 0; i < strlen(buffer); i++)
        {
            state += buffer[i];
        }
       
        if (state == "Not found")
        {
            printf("Message from server: %s", msg);
            cout<< " not found."<<endl<<endl;
        }
        else
        {
            cout<<"Client has received results from Main Server:"<<endl;
            printf("Message from server: %s", msg);
            cout<<" is associated with state "<< state<<endl<<endl;
        }
        cout<<"-----Start a new query-----"<<endl;
    }
    
    close(sock);
    return 0;
}