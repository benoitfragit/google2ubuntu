#dictionnary/Makefile

.SUFFIXES:
.PHONY: clean

OBJ = dictionnary.o

all: $(OBJ)

%o: %c
	gcc -c dictionnary.c -o $(OBJ) `pkg-config --cflags --libs glib-2.0` -O2 -g3 -Werror -lm

clean:
	rm *.o
