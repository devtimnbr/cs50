#include <stdio.h>
#include <stdlib.h>

typedef unsigned char BYTE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover infile\n");
        return 1;
    }

    // Open  input file 
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    FILE *outptr = NULL;
    BYTE buffer[512];

    int jpegCount = 0;

    while (fread(buffer, sizeof(BYTE) * 512, 1, inptr) == 1)
    {
        // Check for start of a new JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close previous JPEG file
            if (outptr != NULL)
            {
                fclose(outptr);
            }

            // Create a new filename
            char filename[8];
            sprintf(filename, "%03d.jpg", jpegCount);

            // Open a new file for writing 
            outptr = fopen(filename, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", filename);
                return 3;
            }

            // Increment JPEG counter
            jpegCount++;
        }

        // Write buffer to current JPEG file
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, outptr);
        }
    }

    // Close last opened JPEG file
    if (outptr != NULL)
    {
        fclose(outptr);
    }

    // Close input file (forensic image)
    fclose(inptr);

    return 0;
}