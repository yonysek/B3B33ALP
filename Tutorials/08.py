x = list(range(10, 0, -1))

y = []
z = []


def hanoi(a, b, c, n):
    if n != 0:
        hanoi(a, c, b, n - 1)
        disc = a.pop()
        c.append(disc)
        print(n, x, y, z)
        hanoi(b, a, c, n - 1)


hanoi(x, y, z, len(x))
