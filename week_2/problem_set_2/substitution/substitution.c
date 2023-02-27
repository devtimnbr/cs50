#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) 
{
    if (argc != 2) 
    {
        printf("Usage: ./substitution key\n");
        return 1;
    } 

    char *key = argv[1];
    int key_length = strlen(key);

    // validate key length
    if (key_length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // validate characters alpha and duplicates
    for (int i = 0; i < key_length; i++) 
    {
        char c = key[i];
        if (!isalpha(c))
        {
            printf("Key must contain 26 alphabetic characters.\n");
            return 1;
        }

        c = tolower(c);
        for (int j = i + 1; j < key_length - 1; j++)
        {
            if (c == tolower(key[j]))
            {
                printf("Key must contain 26 alphabetic characters without duplicates.\n");
                return 1;
            }
        }
    }

    // prompt for plain text
    char *plain = get_string("plaintext: ");

    // encode text and print text
    int plain_length = strlen(plain);
    printf("ciphertext: ");

    for (int i = 0; i < plain_length; i++) 
    {
        char c = plain[i];

        if (isalpha(c))
        {
            int pos = tolower(c) - 'a';

            if (islower(c))
            {
                c = tolower(key[pos]);
            }
            else 
            {
                c = toupper(key[pos]);
            }
        }

        printf("%c", c);
    }

    printf("\n");
}