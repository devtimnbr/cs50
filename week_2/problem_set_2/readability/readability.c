#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);

int count_words(string text);

int count_sentences(string text);

int main(void) 
{
    char *text = get_string("Text: ");
    float letters = count_letters(text);
    float words = count_words(text);
    int sentences = count_sentences(text);

    float l = letters / words * 100;
    float s = sentences / words * 100;

    int grade = round(0.0588 * l - 0.296 * s - 15.8);

    if (grade < 1) 
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16) 
    {
        printf("Grade 16+\n");
    }
    else 
    {
        printf("Grade %i\n", grade);
    }
}

int count_letters(string text)
{
    int letters = 0;
    int length = strlen(text);

    printf("length: %i\n", length);
    for (int i = 0; i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return letters;
}

int count_words(string text) 
{
    int words = 0;
    int length = strlen(text);

    for (int i = 0; i < length; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }

    // add last word
    return words + 1;
}

int count_sentences(string text) 
{
    int sentences = 0;
    int length = strlen(text);

    for (int i = 0; i < length; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }

    return sentences;
}