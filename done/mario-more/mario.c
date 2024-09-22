#include <cs50.h>
#include <stdio.h>

int get_height(void);

int main(void)
{
    int h = get_height();
    int sp = h - 1;
    int st = 1;

    while (st < h + 1)
    {
        for (int i = 0; i < sp; i++)
        {
            printf(" ");
        }
        for (int i = 0; i < st; i++)
        {
            printf("#");
        }

        printf("  ");

        for (int i = 0; i < st; i++)
        {
            printf("#");
        }

        printf("\n");
        sp -= 1;
        st += 1;
    }
}

int get_height(void)
{
    int i;
    do
    {
        i = get_int("Input Height: ");
    }
    while (i < 1 || i > 8);
    return i;
}