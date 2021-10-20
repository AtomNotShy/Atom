# Socket Programingg PA1

## Author: Tong Zhou ID: 6413480147

### Content

This project includes two parts: servermain, client. Run the server firthly. Then in the window of client you can type in a city of America, and the server would receive the message from the client using TCP over port 33147. The server would look up the city in the dictionary which state the city is in and send it back to client using dynamic port, while the city is not in America, server would send Not found to client. The server support Multi-thread, many clients could connect to the main server and look up the city.

use make all to compile the server and client in the terminal

```#bash
Make all 
```

to Bootup the main server

```#bash
./servermain
```  

to open one client

```#bash
./client
```
