import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Read database file into a variable
    database_file = sys.argv[1]
    database = []

    with open(database_file, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            database.append(row)

    # Read DNA sequence file into a variable
    sequence_file = sys.argv[2]

    with open(sequence_file, "r") as file:
        dna_sequence = file.read()

    # Find longest match of each STR in DNA sequence
    matches = {}

    for key in database[0][1:]:
        matches[key] = longest_match(dna_sequence, key)

    # Check database for matching profiles
    match_found = False
    header = database[0][1:] 

    for person in database[1:]:
        is_match = True
        for key in header:            
            if int(person[header.index(key) + 1]) != matches[key]:
                is_match = False
                break
        if is_match:
            print(person[0])
            match_found = True

    if not match_found:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
