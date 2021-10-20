#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <map>

#define MAXIMUM 64
#define PORT 33147 //ID 6413480147
using namespace std;

string states;

map<string, string> city_map;
//create socket
int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
struct sockaddr_in clnt_addr;
socklen_t clnt_addr_size = sizeof(clnt_addr);

void read_data(map<string, string> &city_map)
{
    string state,citys,city;
    ifstream file;
    
    file.open("list.txt");
    bool ret;
    
    while(!file.eof())
    {
        string null;
        getline(file, state, '\r');
        getline(file, null);
        getline(file, citys, '\r');
        cout<<state + ":"<<endl;
        states += state + ",";
        stringstream ss(citys);
        
        while (getline(ss,city,','))
        {
            ret = city_map.insert(pair<string, string>(city, state)).second;
            
            if (ret)
            {
                cout << city << endl;
            }
        }
        getline(file, null);
        null.clear();
        cout<<endl;  
    }
    states.erase(states.end() - 1);
}


void thread_fn(int ID, int clnt_sock){
    while (1)
    {   
        char buffer[MAXIMUM] = {0};
        if (recv(clnt_sock, buffer, 64, 0) == 0) continue;

        string cityname;
        for (int i = 0; i < strlen(buffer); i++)
        {
            cityname += buffer[i];
        }
        int dynamic = clnt_addr.sin_port;
        cout<<"Main server has received the request on city "<< cityname <<" from client"<< ID <<" using TCP over port "<< dynamic <<endl;
        
        string state;
        if (city_map.find(cityname) != city_map.end())
        {
            state = city_map.find(cityname)->second;     
            cout<<cityname<<" is associated with state "<<state<<endl; 
            cout<<"Main Server has sent searching result to client"<< ID <<" using TCP over port "<<"33147"<<endl;
        }
        else
        {
            state = "Not found"; 
            cout<<cityname<<" does not show up in states "<<states<<endl;
            cout<<"Main server has sent \""<< cityname <<": Not found\" to client"<< ID <<" using TCP over port "<< dynamic <<endl;
        }
        char msg[MAXIMUM]={0};
        for (int i = 0; i < state.length(); i++)
        {
            msg[i]=state[i];
        }
        send(clnt_sock, msg, MAXIMUM, 0);
    }
    close(clnt_sock);
}

int main(){
    
    //read city data and saved into city_map
    cout<<"Main server has read the state list from list.txt."<<endl;
    
    read_data(city_map);    

    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));  //fill with 0
    serv_addr.sin_family = AF_INET;  //IPv4
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  //local machine
    serv_addr.sin_port = htons(33147);  
    bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

    //listen user
    listen(serv_sock, 20);

    int n = 1;
    while (int clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size))
    {
        pid_t pid;
        pid = fork();      
        if (pid == 0)
        {
            thread_fn(n, clnt_sock);   
            exit(0);
        }
        else if (pid < 0)
        {
            perror("fork error");
            exit(1);
        }
        n++;
    } 

    close(serv_sock);
    return 0;
}