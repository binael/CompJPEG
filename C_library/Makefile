CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=gnu89

.PHONY: clean
%.o: %.c %.h
	$(CC) $(CFLAGS) -c -fPIC -o $@ $<

liball.so: $(patsubst %.c, %.o, $(wildcard *.c))
	$(CC) $(CFLAGS) -shared $^ -o $@

all: liball.so

clean:
	rm -f %.o
