/*
 * This is an example for how-to use the kernel monitor for watermarking code:
 * 
 * Compiled as:
 *
 *   gcc -Wall -m32 -o watermarked_test_with_km kernel_monitor/test.c -lm
 *
 */

#include <unistd.h>
#include <fcntl.h>

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <assert.h>

#define DEVICE_NAME "/dev/execution-trace-monitor"

int device_fd = -1;

void initialize()
{
	device_fd = open(DEVICE_NAME, O_RDWR);

	if (device_fd < 0) {
		exit(EXIT_FAILURE);
	}
}

void update_watermark(int bit)
{
	assert (bit == 0 || bit == 1);

	/* transform to char */
	char c = bit + '0';
	write(device_fd, &c, 1);
}

int get_next_block_number(void)
{
	int bits = 0;

	read(device_fd, &bits, sizeof bits);

	return bits;
}

int main(void)
{
	int x = 13;

	initialize();

	/* this full of opaque is just an example */

	if (sin(x) < 2) {
		update_watermark(1);
	} else {
		update_watermark(0);
	}

	if (x*x < 0) {
		update_watermark(1);
	} else {
		update_watermark(0);
	}

	int y = x*(x+1)*(x+2);
	if (y % 3 == 0) {
		update_watermark(1);
	} else {
		update_watermark(0);
	}

	int next = get_next_block_number();

	printf("next number from the kernel monitor is %d\n", next);

	return 0;
}
