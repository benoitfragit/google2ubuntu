#task/Makefile

.SUFFIXES:
.PHONY: clean

OBJ = processor.o

all: $(OBJ)

%o: %c
	gcc -c processor.c -o processor.o `pkg-config --cflags --libs glib-2.0` -O2 -g3 -Werror -lm

clean:
	rm *.o
