CRC(cyclic redundancy check) and checksum realization by c++

Author: Tong Zhou #6413480147


How to calculate crc:

I used vectors to save the message and generator. initialise the remainder by divding(Xor) the first 13 elements of message by crc generator. Then each time, I pull one element from message, and remove the first element in the remainder, only if the first element is not zero. Finally, the remainder is the crc.

How to calculate checksum:
transmit every 8 bits of message into decimal number, add them together, we get the sum. q=sum/256, r=sum%256, only if r+q is less than 255, then transmit(255- (q+r)) to binary number of 8 bits. Then the binary number is checksum of the message.

This project realized CRC and checksum by c++, there are three files.

crc_tx: the function of this file is to read data waiting for transmistion, and produce a crc for each message.

crc_rx: the function is to read each line of the receiving message, and then check if the crc is crorrect by recalculate the message, if the crc is same, then display pass, else not pass.

crc_vs_checksum: read the original message, and calculate transmistion crc and checksum. Apply the errors to the data with crc, data with checksum. Then calculate if crc check is crorrect, calculate if the checksum is crorrect

idiosyncrasy: for each message, the function needs to be initialised, or the old data would interference the present function. After debugging many times, I find the problem and fixed it.
