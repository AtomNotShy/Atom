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
    vector<int>message,remainder,crc;
    ifstream file;
    file.open("dataRx.txt");
    while (getline(file, str))
    {

        int len = str.size();
 
        for (int i = 0; i < len-12; i++) //string to int and saved into vector
        {
           temp = str.at(i);
           message.push_back(temp-'0');
        }
        message.insert(message.end(),12,0);

        for (int i = len-12; i < len; i++) //string to int and saved into vector
        {
           temp = str.at(i);
           crc.push_back(temp-'0');
        }

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

        remainder.erase(remainder.begin());

       if (remainder==crc)
       {
          cout<<"pass"<<endl;
       }
       else
       {
           cout<<"not pass"<<endl;
       }

        message.clear();
        remainder.clear();
        crc.clear(); //clear vectors


    }

    
    return 0;

}
