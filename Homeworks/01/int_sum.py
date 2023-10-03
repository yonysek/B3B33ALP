
a = int(input())
b = int(input())


sum = 0

if a <= b:
  for i in range(a, b + 1):
    sum += i**4
else:
  for i in range(b, a + 1):
    sum += i**4


print(sum)