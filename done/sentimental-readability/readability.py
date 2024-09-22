def main():
    text = input("Input: ")
    L, W, S = analyse(text)
    index = round(0.0588 * (100.0 * L / W) - 0.296 * (100.0 * S / W) - 15.8)
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def analyse(str):
    L = S = 0
    W = 1
    for i in str:
        if i.isalpha():
            L += 1
        elif i == " ":
            W += 1
        elif i == "." or i == "!" or i == "?":
            S += 1
    return L, W, S


main()
