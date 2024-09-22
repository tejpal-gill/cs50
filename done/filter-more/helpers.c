#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int grey = round((image[h][w].rgbtRed + image[h][w].rgbtGreen + image[h][w].rgbtBlue) / 3.0);
            image[h][w].rgbtRed = image[h][w].rgbtGreen = image[h][w].rgbtBlue = grey;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int s = 1;
    RGBTRIPLE tmp;
    if (width > 2)
    {
        s = floor(width / 2.0);
    }
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < s; w++)
        {
            tmp = image[h][w];
            image[h][w] = image[h][width - (w + 1)];
            image[h][width - (w + 1)] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE img[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            img[i][j] = image[i][j];
        }
    }
    // intiating bluring
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            int r = 0, g = 0, b = 0;
            float c = 0;
            for (int i = h - 1; i < h + 2; i++)
            {
                for (int j = w - 1; j < w + 2; j++)
                {
                    if (i >= 0 && i < height && j >= 0 && j < width)
                    {
                        r += img[i][j].rgbtRed;
                        g += img[i][j].rgbtGreen;
                        b += img[i][j].rgbtBlue;
                        c++;
                    }
                }
            }
            image[h][w].rgbtRed = round(r / c);
            image[h][w].rgbtGreen = round(g / c);
            image[h][w].rgbtBlue = round(b / c);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE img[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            img[i][j] = image[i][j];
        }
    }
    // sophisticated edge detection
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            for (int c = 0; c < 3; c++)
            {
                int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
                int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
                for (int i = h - 1, x = 0; i < h + 2; i++, x++)
                {
                    for (int j = w - 1, y = 0; j < w + 2; j++, y++)
                    {
                        if (i < 0 || i == height || j < 0 || j == width)
                        {
                            Gx[x][y] = 0;
                            Gy[x][y] = 0;
                            continue;
                        }
                        if (c == 0)
                        {
                            Gx[x][y] = Gx[x][y] * img[i][j].rgbtRed;
                            Gy[x][y] = Gy[x][y] * img[i][j].rgbtRed;
                        }
                        else if (c == 1)
                        {
                            Gx[x][y] = Gx[x][y] * img[i][j].rgbtGreen;
                            Gy[x][y] = Gy[x][y] * img[i][j].rgbtGreen;
                        }
                        else if (c == 2)
                        {
                            Gx[x][y] = Gx[x][y] * img[i][j].rgbtBlue;
                            Gy[x][y] = Gy[x][y] * img[i][j].rgbtBlue;
                        }
                    }
                }
                int tmpx = 0, tmpy = 0;
                for (int x = 0; x < 3; x++)
                {
                    for (int y = 0; y < 3; y++)
                    {
                        tmpx += Gx[x][y];
                        tmpy += Gy[x][y];
                    }
                }
                int value = round(sqrt(tmpx * tmpx + tmpy * tmpy));
                if (value > 255)
                {
                    value = 255;
                }
                if (c == 0)
                {
                    image[h][w].rgbtRed = value;
                }
                else if (c == 1)
                {
                    image[h][w].rgbtGreen = value;
                }
                else if (c == 2)
                {
                    image[h][w].rgbtBlue = value;
                }
            }
        }
    }
    return;
}
