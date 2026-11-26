def is_positive_two_digit(x):
    return 10 <= x <= 99


with open('examples/17.txt', 'r') as f:
    nums = [int(x) for x in f.read().split()]

# Минимальное положительное двузначное число последовательности
two_digit_numbers = [x for x in nums if is_positive_two_digit(x)]

if not two_digit_numbers:
    # Если положительных двузначных чисел нет, условие делимости невыполнимо
    print(0)
    print(0)
else:
    divisor = min(two_digit_numbers)

    count = 0
    max_sum = None
    n = len(nums)

    # Пары на расстоянии не менее двух позиций: j - i >= 2
    for i in range(n):
        for j in range(i + 2, n):
            a = nums[i]
            b = nums[j]

            # Ровно один элемент пары — положительное двузначное число
            if is_positive_two_digit(a) != is_positive_two_digit(b):
                pair_sum = a + b

                # Сумма должна делиться без остатка на divisor
                if pair_sum % divisor == 0:
                    count += 1
                    if max_sum is None or pair_sum > max_sum:
                        max_sum = pair_sum

    if max_sum is None:
        max_sum = 0

    print(count)
    print(max_sum)