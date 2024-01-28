count = 6
x = [23, 12, 13, 17, 24, 19]
m = 0
for i in range(count):
    if x[i] > x[m]:
        m = i

print(m)
