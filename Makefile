.PHONY:all

all:
	$(CC) fibonacci.c -c -o fibonacci.o -ggdb3
	$(CC) fibonacci_main.c -c -o fibonacci_main.o -ggdb3
	$(CC) wm_fibonacci.c -c -o wm_fibonacci.o -ggdb3
	$(CC) fibonacci.o fibonacci_main.o -o fib -ggdb3
	$(CC) wm_fibonacci.o fibonacci_main.o -o wm_fib -ggdb3

