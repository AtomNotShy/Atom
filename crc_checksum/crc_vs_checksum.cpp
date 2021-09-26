#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
#include <sstream>
#include <cmath>

using namespace std;

int poly[13] = {1,1,0,0,0,0,0,0,0,1,1,1,1};

vector<int>strtovec(string ss)      // transmit string to vector
{
    vector<int>data;
    for (int i = 0; i < ss.length(); i++)
    {
        data.push_back(ss[i]-'0');  
    }
    
    return data;
}
vector<int>cal_crc(vector<int>orig_message)        //calculate crc for sending message

{
    vector<int>remainder;
    orig_message.insert(orig_message.end(),12,0);

    if (orig_message[0]==0) // remove the zeros in the first pos
    {
        orig_message.erase(orig_message.begin());
    }
        
    for (int i = 0; i <=12; i++) //get the first 12 codes and make an xor action saved into remainder
    {  
        remainder.push_back(poly[i] ^ orig_message[i]);  
    }

    for (int n = 13; n < orig_message.size(); n++)  // iterate the following elements by bit
        {
        remainder.erase(remainder.begin());
        remainder.push_back(orig_message[n]);
            
        if (remainder[0]) //tell if the first element is 1 else keep moving the next element
        {
            for (int i=0; i <= 12; i++)
            {
                remainder[i] ^=  poly[i];
            }
                
        }
        
        }
        remainder.erase(remainder.begin());
        return remainder;
}

vector<int>cal_crc2(vector<int>orig_message)        //calculate crc for recevied message 

{
    vector<int>remainder;

    if (orig_message[0]==0) // remove the zeros in the first pos
    {
        orig_message.erase(orig_message.begin());
    }
        
    for (int i = 0; i <=12; i++) //get the first 12 codes and make an xor action saved into remainder
    {  
        remainder.push_back(poly[i] ^ orig_message[i]);  
    }

    for (int n = 13; n < orig_message.size(); n++)  // iterate the following elements by bit
        {
        remainder.erase(remainder.begin());
        remainder.push_back(orig_message[n]);
            
        if (remainder[0]) //tell if the first element is 1 else keep moving the next element
        {
            for (int i=0; i <= 12; i++)
            {
                remainder[i] ^=  poly[i];
            }
                
        }
        
        }
        remainder.erase(remainder.begin());
        return remainder;
}

vector<int>cal_checksum(vector<int>orig_message)       //calculate checksum
{
    int sum,q,r;
    vector<int>checksum;

    for (int i = 0; i < orig_message.size(); i+=8)
    {
        sum += orig_message[i]*0x80 +orig_message[i+1]*0x40 +orig_message[i+2]*0x20 +orig_message[i+3]*0x10 +orig_message[i+4]*0x08 +orig_message[i+5]*0x04 +orig_message[i+6]*2 +orig_message[i+7]*1;
        
    }
    q=sum/256;
    r=sum%256;
    if (r+q>255)
    {
        q=(r+q)/256;
        r=(r+q)%256;
    }

    sum = 255-(r+q);
    for (int i = 0; i < 8; i++)
    {
        checksum.insert(checksum.begin(),sum%2);
        sum/=2;
    }
    return checksum;
}
vector<int>add_error(vector<int>error,vector<int>codeword)      //add transmiting errors
{
    for (int i = 0; i < error.size(); i++)
        {
          codeword[i]^=error[i];
        }
    return  codeword;   
}
void print_vec(vector<int>infor)
{
    for (int i = 0; i < infor.size(); i++)  //print crc
        {
            cout<<infor[i];
        }

}

void tell(vector<int>new_remainder,vector<int>zero)  //tell if the crc as same as crc with transmition error
{
    if (new_remainder!=zero) 
        {
           cout<<"not pass"<<endl;
        }
        else
        {
           cout<<"pass"<<endl; 
        }
}

int main()
{
    string line,str,error_s;
    int temp = 0;
    vector<int>orig_message,remainder,crc_codeword,checksum_codeword,checksum,error,crc_codeword_error,checksum_codeword_error,new_remainder, new_checksum;
    vector<int>zero;
    zero.insert(zero.end(),12,0);
    ifstream file;
    file.open("dataVs.txt");
    while (getline(file, line))
    {
        stringstream linestream(line);
        linestream >> str;
        linestream >> error_s;
        orig_message= strtovec(str);
        error = strtovec(error_s);
        remainder =cal_crc(orig_message);  // sending crc
        checksum = cal_checksum(orig_message); // sending checksum

        crc_codeword.insert(crc_codeword.end(),orig_message.begin(),orig_message.end());
        crc_codeword.insert(crc_codeword.end(),remainder.begin(),remainder.end());  //get the transmited codeword with crc 
        crc_codeword_error = add_error(error,crc_codeword);         // add errors on the whole message
        new_remainder = cal_crc2(crc_codeword_error);

        checksum_codeword.insert(checksum_codeword.end(),orig_message.begin(),orig_message.end());
        checksum_codeword.insert(checksum_codeword.end(),checksum.begin(),checksum.end()); //get the transmited codeword with checksum
        checksum_codeword_error = add_error(error,checksum_codeword);

        checksum_codeword.clear();
        checksum_codeword.insert(checksum_codeword.begin(),checksum_codeword_error.begin(),checksum_codeword_error.end()-8);
        checksum.clear();
        checksum.insert(checksum.begin(),checksum_codeword_error.end()-8,checksum_codeword_error.end());
        new_checksum = cal_checksum(checksum_codeword);

        cout<<"crc : ";
        print_vec(remainder);
        cout<<"  result: ";
        tell(new_remainder,zero);
        cout<<"checksum: ";    //print checksum
        print_vec(checksum);
        cout<<"  result: ";
        tell(checksum,new_checksum);
        cout<<endl;

        orig_message.clear();
        remainder.clear();
        crc_codeword.clear();
        checksum_codeword.clear();
        checksum,error.clear();
        crc_codeword_error.clear();
        checksum_codeword_error.clear();
        new_remainder.clear();
        new_checksum.clear();


    }

}