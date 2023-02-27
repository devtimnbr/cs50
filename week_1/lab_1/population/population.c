#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start, end;
    // TODO: Prompt for start size
    do {
        start = get_int("Insert the start size: ");
    } while (start < 9);
    
    // TODO: Prompt for end size
    do {
        end = get_int("Insert the end size: ");
    } while (end < start);
    // TODO: Calculate number of years until we reach threshold
    int population = start;
    int years = 0;

    while(population < end) {
        population += (population / 3) - (population / 4);
        years++;
    }
    // TODO: Print number of years
    printf("Years: %i\n", years);
}
