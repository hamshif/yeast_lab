CCFLAGS = -I. -I/usr/local/include  -Wall -Wno-sign-compare `pkg-config --cflags opencv` -m64
LIBFLAGS = `pkg-config --libs opencv` -m64

CC = g++ -g $(CCFLAGS)
LD = g++ -g $(LIBFLAGS)

OBJ = linreg.o

Process: Process.o linreg.o
	$(LD) -o $@ Process.o linreg.o

%.o: %.cpp
	$(CC) -c -o $@ $<

clean:
	rm -f Process *.o

