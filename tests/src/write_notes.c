#include <stdio.h>
#include <string.h>

/* Build: gcc write_notes.c -o write_notes.exe */

int main() {
    const int n = 5;
    char lines[n][200];
    for (int i = 0; i < n; i++) {
        fgets(lines[i], sizeof(lines[i]), stdin);
        lines[i][strlen(lines[i])-1] = '\0';
    }
    for (int i = 0; i < n; i++) {
        printf("Line #%02d: %s\n", i + 1, lines[i]);
    }
    return 0;
}
