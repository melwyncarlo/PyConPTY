#include <stdio.h>

/* Build: gcc print_lines_of_text.c -o print_lines_of_text.exe */

int main() {
    printf("This is line 1 with newline.     \n");
    printf("This is line 2 with newline.\n");
    printf("This is line 3 with newline.\n");
    printf("\n");
    printf("This is line 5 with newline.\n");
    printf("This is line 6 WITHOUT newline.     ");
    return 0;
}
