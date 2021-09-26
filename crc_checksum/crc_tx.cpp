#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>

using namespace std;
int poly[13] = {1,1,0,0,0,0,0,0,0,1,1,1,1};

int main()
{
    string str;
    int temp = 0;
    vector<int>message,remainder;

    ifstream file;
    file.open("dataTx.txt");

    while (getline(file, str))
    {
        file>>str;
        cout<<"codeword:"<<endl;
        cout<<str<<endl;
 
        for (int i = 0; i < str.size(); i++) //string to int and saved into vector
        {
           temp = str.at(i);
           message.push_back(temp-'0');
        }
        message.insert(message.end(),12,0);
        if (message[0]==0) // remove the zeros in the first pos
        {
            message.erase(message.begin());
        }
        
        for (int i = 0; i <=12; i++) //get the first 12 codes and make an xor action saved into remainder
        {  
          remainder.push_back(poly[i] ^ message[i]);  
        }

        for (int n = 13; n < message.size(); n++)  // iterate the following elements by bit
        {
            remainder.erase(remainder.begin());
            remainder.push_back(message[n]);
            
            if (remainder[0]) //tell if the first element is 1 else keep moving the next element
            {
                for (int i=0; i <= 12; i++)
                {
                    remainder[i] ^=  poly[i];
                }
                
            }
        
        }
        cout<<"crc:"<<endl;

        for (int i = 1; i <remainder.size(); i++)
        {

            cout<<remainder[i];
        }
        cout<<endl;

        message.clear();//clear vectors
        remainder.clear();
    }
    return 0;

}
