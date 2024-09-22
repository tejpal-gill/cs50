#include <cs50.h>
#include <stdio.h>

int get_asize(void);
int get_bsize(int a);

int main(void)
{
    int n = 0;

    // TODO: Prompt for start size
    int a = get_asize();

    // TODO: Prompt for end size
    int b = get_bsize(a);

    // TODO: Calculate number of years until we reach threshold
    while (a < b)
    {
        a = a + (a / 3) - (a / 4);
        n++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", n);
}

int get_asize(void)
{
    int a;
    do
    {
        a = get_int("Start Size: ");
    }
    while (a < 9);

    return a;
}

int get_bsize(int a)
{
    int b;
    do
    {
        b = get_int("End Size: ");
    }
    while (a > b);

    return b;
}