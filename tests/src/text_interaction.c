#include <stdio.h>
#include <string.h>

/* Build: gcc text_interaction.c -o text_interaction.exe */

int main() {
    char name[200] = {0};
    int age;
    printf("What is your name? ");
    fgets(name, sizeof(name), stdin);
    name[strlen(name)-1] = '\0';
    printf("Hi, %s! What's your age? ", name);
    scanf("%d", &age);
    printf("Hmm, so you will be %d years old in 10 years.", age + 10);
    return 0;
}
