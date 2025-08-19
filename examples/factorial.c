#include <stdio.h>

int get_factorial(int number) {
    if (number < 0) {
        return -1;
    } else if ((number == 0) || (number == 1)) {
        return 1;
    } else {
        int factorial = 1;
        for (int i = 1; i <= number; i++) {
            factorial *= i;
        }
        return factorial;
    }
}

int main() {
    int number;
    printf("\n Compute the factorial of: ");
    scanf("%d", &number);
    const int factorial = get_factorial(number);
    if (factorial == -1) {
        printf(" !%d = %s\n", number, "undefined");
    } else {
        printf(" !%d = %d\n", number, factorial);
    }
    return 0;
}
