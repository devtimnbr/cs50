height = 0

while height < 1 or height > 8:
    try:
        height = int(input("Height: "))
    except:
        print("Invalid height")

for i in range(1, height + 1):
    # gaps + hashtags + big gap + hashtags
    print((height - i) * " " + "#" * i + "  " + "#" * i)

