def sexy_primes():
    primes = []
    for i in range(2, 1000):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            primes.append(i)

    for i in range(len(primes)):
        if primes[i] - 6 in primes:
            print(primes[i] - 6, primes[i])


# sexy_primes()


# def find_divisors(n):
#     divisors = []
#     for i in range(1, n):
#         if n % i == 0:
#             divisors.append(i)
#     return divisors


# def perfect_numbers(x):
#     for i in range(2, x):
#         if i**2 > x:
#             break
#         if sum(find_divisors(i)) == i:
#             print(i)


# def sum_of_divisors(x):
#     sum = 1
#     for i in range(2, x):
#         if i**2 > x:
#             break
#         if x % i == 0:
#             sum += i
#             if i != x // i:
#                 sum += x // i
#             return sum


# for i in range(1, 10000):
#     print(sum_of_divisors(i))

# TODO sexy_primes() and perfect_numbers() and super_perfect_numbers()


def gcd1(a, b):
    if a < b:
        a, b = b, a
    while a > b:
        print(a, b)
        a = a - b
        if a < b:
            a, b = b, a
    return a


# print(gcd1(21, 14))


def gcd2(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


print(gcd2(14, 21))
