from cs50 import get_string


def main():
    n = get_string("Number: ")
    t = n[:2]
    l = len(n)
    if check_sum(n) == 0 or (l != 13 and l != 15 and l != 16):
        print("INVALID")
    elif t == "34" or t == "37":
        print("AMEX")
    elif int(t) > 50 and int(t) < 56:
        print("MASTERCARD")
    elif t[0] == "4":
        print("VISA")
    else:
        print("INVALID")


def check_sum(n):
    c = t = 0
    for i in n[-2::-2]:
        c = int(i) * 2
        if c > 9:
            c = str(c)
            t = t + int(c[0]) + int(c[1])
        else:
            t = t + c
    for i in n[-1::-2]:
        t = t + int(i)
    print(t)
    if t % 10 == 0:
        return 1
    else:
        return 0


main()
