def count_letters(text):
    return sum(1 for char in text if char.isalpha())

def count_words(text):
    return len(text.split())

def count_sentences(text):
    # loops each char in text and sums up .?! by one
    return sum(1 for char in text if char in ['.', '?', '!'])

def main():
    text = input("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    l = letters / words * 100
    s = sentences / words * 100

    grade = round(0.0588 * l - 0.296 * s - 15.8)

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")

if __name__ == "__main__":
    main()
