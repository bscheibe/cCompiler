#include <stdio.h>

void print_it(int n1, int n2, int n3, double av);
double av(int a, int b, int);

main(void)
{
        int n1, n2, n3;

        printf("Enter: ");
        scanf("%d %d %d", &n1, &n2, &n3);

        print_it(n1, n2, n3, av(n1, n2, n3));
}

void print_it(int n1, int n2, int n3, double av)
{
        printf("Mean %d %d %d is %f\n",
                n1, n2, n3, av);
}

double av(int n1, int n2, int n3)
{
        double sum;

        sum = n1 + n2 + n3;
        return sum / 3.0;
}