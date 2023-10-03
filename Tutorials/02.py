# t = int(input())
t = 100000

days = t // (3600 * 24)
t = 100000 % (3600 * 24)

hours = t // 3600
t = t % 3600

minutes = t // 60
t = t % 60

seconds = t

print(days, hours, minutes, seconds)


def move_decimal(float_num, power):
    # Convert the float to a string
    float_str = str(float_num)

    integer_part, _, fractional_part = float_str.partition(".")

    if power < 0:
        adjusted_str = "0." + "0" * abs(abs(power) - 1) + integer_part + fractional_part
    else:
        adjusted_str = integer_part + fractional_part + "0" * power

    return adjusted_str


print(move_decimal(1.10111, -2))
