DDLCCDLL_Linux: DDLCCDLL_Linux.cpp
	# compile the actual so lib
	g++ -std=c++11 -c -Werror -fpic -o DDLCCDLL_Linux.o DDLCCDLL_Linux.cpp
	g++ -shared -o DDLCCDLL_Linux.so DDLCCDLL_Linux.o
	# Add to renpy project
	cp DDLCCDLL_Linux.so ../RenpyProject/game
