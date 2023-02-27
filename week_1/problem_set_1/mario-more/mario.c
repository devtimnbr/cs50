#include <cs50.h>
#include <stdio.h>

/*
    1. Pompt for height
    2. Loop through height
    2.1. Print left spaces
    2.2. Print left hashtags
    2.3. Print gap
    2.4. Print right hashtags
    2.6 Print new Line
 */

int main(void)
{
    int height;
    // prompt for height
    do
    {
        height = get_int("Insert the height: ");
    } 
    while (height < 1 || height > 8);

    // print pyramids
    for (int i = 0; i < height; i++)
    {
        // print left spaces
        for (int j = height - 1; j > i; j--)
        {
            printf(" ");
        }

        // print left hashtags
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // print gap
        printf("  ");

        // print right hashtags
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}