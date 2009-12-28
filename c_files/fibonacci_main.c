#include <stdio.h>

extern int fibonacci(int n);

int main(void)
{
	int i = 0;

	while (i<10)
		printf("%d, ", fibonacci(i++));

	printf("%d\n", fibonacci(i));

	return 0;
}
