#include "phash.h"
#include <stdio.h>
#include <assert.h>

long long hash(int n1, int n2, double *data)
{
    int i, j, k, l;
    long long x;

    assert (n1 == 32 && n2 == 64);

    double sum = 0, sum1;
    for (i = 0; i < n1; i++) {
        for (j = 0; j < n2; j++) {
           sum = sum + data[i * n2 + j];
        }
    }
    sum /= 64;
    x = 0;
    for (i = 0; i < n1; i+=4) {
        for (j = 0; j < n2; j+=8) {
            sum1 = 0;
            for (k = 0; k < 4; k++) {
                for (l = 0; l < 8; l++) {
                    sum1 = sum1 + data[(i + k) * n2 + j + l];
                }
            }
            x <<= 1;
            if (sum1 > sum) {
                x |= 0x1;
            }
        }
    }
    return x;
}
