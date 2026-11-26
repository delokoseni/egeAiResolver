
def is_positive_two_digit(number: int) -> bool:
    return 10 <= number <= 99


def solve_sequence(numbers: list[int]) -> dict:
    if not numbers:
        raise ValueError("Последовательность пустая")

    two_digit_numbers = [
        number
        for number in numbers
        if is_positive_two_digit(number)
    ]

    if not two_digit_numbers:
        raise ValueError(
            "В последовательности нет положительных двузначных чисел"
        )

    minimum_two_digit = min(two_digit_numbers)

    pair_count = 0
    maximum_pair_sum = None

    for i in range(len(numbers)):
        for j in range(i + 2, len(numbers)):

            first = numbers[i]
            second = numbers[j]

            exactly_one_two_digit = (
                is_positive_two_digit(first)
                != is_positive_two_digit(second)
            )

            if not exactly_one_two_digit:
                continue

            pair_sum = first + second

            if pair_sum % minimum_two_digit != 0:
                continue

            pair_count += 1

            if (
                maximum_pair_sum is None
                or pair_sum > maximum_pair_sum
            ):
                maximum_pair_sum = pair_sum

    return {
        "minimum_two_digit": minimum_two_digit,
        "pair_count": pair_count,
        "maximum_pair_sum": maximum_pair_sum
    }
