#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

string text;
int L = 0;
int W = 1;
int S = 0;
int analyse(string str);

int main(void)
{
    // get text
    text = get_string("Input: ");

    // analyse
    analyse(text);

    // formula
    int index = round(0.0588 * (100.0 * L / W) - 0.296 * (100.0 * S / W) - 15.8);

    // print
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int analyse(string str)
{
    int len = strlen(str);
    for (int i = 0; i < len; i++)
    {
        char word = str[i];
        if (isalpha(word))
        {
            L++;
        }
        else if (word == ' ')
        {
            W++;
        }
        else if (word == '.' || word == '!' || word == '?')
        {
            S++;
        }
    }
    return 0;
}