CC = clang++
FLAGS = -std=c++17 -Wshadow -Wall -O2 -Wno-unused-result
OUT = cgp

default:
	$(CC) $(FLAGS) -O2 -o $(OUT) $(OUT).cpp

debug:
	$(CC) $(FLAGS) -O0 -ggdb3 -o $(OUT) $(OUT).cpp
