all: compile 
compile:
	g++ -o client client.cpp
	g++ -o servermain servermain.cpp
