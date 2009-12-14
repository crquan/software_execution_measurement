
int fibonacci(int n)
{
	int sum; 
    int prev;
	int i;

    sum = 1;
    prev = 1;

	for (i = 1; i <= n; i++) {
		sum += prev;
		prev = sum - prev;
	}

	return sum;
}
