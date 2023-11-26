card_number = 0

# GET CARD NUMBER
while card_number < 1:
    try:
        card_number = int(input("Number: "))
    except ValueError:
        print("Invalid card number")

# INIT VALUES
card_length = len(str(card_number))
tmp_card_number = card_number
checksum = 0

# CALCULATE CHECKSUM
for i in range(0, card_length):
    digit = tmp_card_number % 10
    tmp_card_number //= 10  

    if i % 2 == 0:
        checksum += digit
    else:
        digit *= 2
        checksum += digit // 10 + digit % 10

# CHECK CHECKSUM AND EXIT IF INVALID
if checksum % 10 != 0:
    print("INVALID")
    exit()

# GET START DIGITS
start_digits = card_number

for i in range(0, card_length - 2):
    start_digits //= 10  

# CHECK FOR PROVIDER
if card_length == 15 and (start_digits == 34 or start_digits == 37):
    print("AMEX")
elif card_length == 16 and (51 <= start_digits <= 55):  # Simplify the check for MASTERCARD
    print("MASTERCARD")
elif (card_length == 13 or card_length == 16) and start_digits // 10 == 4:  # Use integer division here
    print("VISA")
else:
    print("INVALID")