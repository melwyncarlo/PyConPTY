#include <stdio.h>

/* Build: gcc print_many_lines_of_text.c -o print_many_lines_of_text.exe */

int main() {
    for (int i = 0; i < 100; i++) {
        printf("Log %d: This is line %d.\n", 100 + i + 1, i + 1);
    }
    return 0;
}
