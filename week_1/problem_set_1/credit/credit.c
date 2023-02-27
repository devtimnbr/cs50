#include <cs50.h>
#include <stdio.h>

int main(void) 
{
    long card_number;

    // PROMPT FOR CARD NUMBER
    do 
    {
        card_number = get_long("Number: ");
    } 
    while (card_number < 1);

    // GET CARD LENGTH
    long card_length_tmp = card_number;
    int card_length = 0;

    while (card_length_tmp > 0) 
    {
        card_length_tmp = card_length_tmp / 10;
        card_length++;
    }

    
    // GET CHECKSUM
    int checksum = 0;
    long tmp_card_number = card_number;

    for (int i = 0; i < card_length; i++) 
    {
        int digit = tmp_card_number % 10;
        tmp_card_number /= 10;

        if (i % 2 == 0) 
        {
            checksum += digit;
        } 
        else 
        {
            digit *= 2;
            checksum += digit / 10 + digit % 10;
        }
    }

    // CHECK CHECKSUM AND RETURN IF INVALID
    if (checksum % 10 != 0) 
    {
        printf("INVALID\n");
        return false;
        
    }

    // GET START DIGITS
    long start_digits = card_number;

    for (int i = 0; i < card_length - 2; i++) 
    {
        start_digits /= 10;
    }
    
    // CHECK FOR PROVIDER
    if (card_length == 15 && (start_digits == 34 || start_digits == 37)) 
    {
        printf("AMEX");
    } 
    else if (card_length == 16 && (start_digits == 51 || start_digits == 52 || start_digits == 53 || start_digits == 54 
                                   || start_digits == 55)) 
    {
        printf("MASTERCARD");
    } 
    else if ((card_length == 13 || card_length == 16) && start_digits / 10 == 4) 
    {
        printf("VISA");
    } 
    else 
    {
        printf("INVALID");
    }
     
    printf("\n");
}