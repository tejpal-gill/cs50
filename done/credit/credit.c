#include <cs50.h>
#include <stdio.h>

int check_sum(long n);
int check_length(long n);
long f_two(long n);

int main(void)
{
    // get card num and first two digits
    long n = get_long("Number: ");
    int t = f_two(n);

    // check card sum & length
    int l = check_length(n);
    if (check_sum(n) != 1 || (l != 13 && l != 15 && l != 16))
    {
        printf("INVALID\n");
    }

    // print card type
    else if (t == 34 || t == 37)
    {
        printf("AMEX\n");
    }

    else if (t > 50 && t < 56)
    {
        printf("MASTERCARD\n");
    }

    else if (t / 10 == 4)
    {
        printf("VISA\n");
    }

    else
    {
        printf("INVALID\n");
    }
}

int check_sum(long n)
{
    int r = 0, t = 0;

    do
    {
        t = n % 10;
        r = r + t;
        n = n / 10;
        t = 2 * (n % 10);
        if (t < 10)
        {
            r = r + t;
        }
        else
        {
            r = r + t % 10;
            r = r + t / 10;
        }
        n = n / 10;
    }
    while (n > 0);

    if (r % 10 == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int check_length(long n)
{
    int i = 0;
    do
    {
        n = n / 10;
        i++;
    }
    while (n > 1);
    return i;
}

long f_two(long n)
{
    do
    {
        n = n / 10;
    }
    while (n > 100);
    return n;
}