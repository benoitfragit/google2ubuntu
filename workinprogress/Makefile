# Makefile racine
.SUFFIXES:
.PHONY:
 
LD = gcc
LDFLAGS =
OBJ = processor/*.o dictionnary/*.o *.o
INCLUDES = -Idictionnary/ -Iprocessor/
 
all:
	make -C processor
	make -C dictionnary
	gcc -c main.c -o main.o `pkg-config --cflags --libs glib-2.0` -O2 -g3 -Werror -lm $(INCLUDES)	
	gcc $(OBJ) -o main `pkg-config --cflags --libs glib-2.0` -O2 -g3 -Werror -lm $(INCLUDES)

clean:
	make -C processor clean
	make -C dictionnary clean
	rm -rf *.o
