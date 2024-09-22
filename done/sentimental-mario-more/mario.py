from cs50 import get_int


def main():
    h = get_height()
    sp = h - 1
    st = 1

    while st < h + 1:
        print(" " * sp, end="")
        print("#" * st, end="  ")
        print("#" * st)
        sp -= 1
        st += 1


def get_height():
    while True:
        h = get_int("Height : ")
        if h > 0 and h < 9:
            return h


main()
