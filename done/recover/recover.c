#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }
    int jpgc = 0;
    BYTE buffer[512];
    FILE *img = NULL;
    char filename[8];
    while (fread(&buffer, 512, 1, file) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpgc != 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", jpgc);
            img = fopen(filename, "w");
            jpgc++;
        }
        if (jpgc != 0)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }
    fclose(file);
    fclose(img);
    return 0;
}