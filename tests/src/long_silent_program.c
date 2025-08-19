#include <stdio.h>
#include <stdint.h>

/* Build: gcc long_silent_program.c -o long_silent_program.exe */

int main() {
    for (int n = 0; n < 1E7; n++) {
        int j = 0;
        for (int i = 0; i < 20; i++) {
            j--;
            uint64_t factorial = 1;
            for (int k = 1; k <= i; k++) {
                factorial *= k;
            }
        }
    }
    return 0;
}
