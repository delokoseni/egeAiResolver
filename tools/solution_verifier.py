from itertools import combinations

def verify_sequence(numbers: list[int]) -> dict:
    if not numbers:
        raise ValueError("Последовательность пустая")

    positive_two_digit = [
        number for number in numbers
        if 10 <= number <= 99
    ]

    if not positive_two_digit:
        raise ValueError(
            "В последовательности нет положительных двузначных чисел"
        )

    minimum_two_digit = min(positive_two_digit)

    valid_pairs = []

    for (i, first), (j, second) in combinations(
        enumerate(numbers), 2
    ):
        if j - i < 2:
            continue

        first_is_two_digit = 10 <= first <= 99
        second_is_two_digit = 10 <= second <= 99

        if first_is_two_digit == second_is_two_digit:
            continue

        pair_sum = first + second

        if pair_sum % minimum_two_digit == 0:
            valid_pairs.append(pair_sum)

    return {
        "minimum_two_digit": minimum_two_digit,
        "pair_count": len(valid_pairs),
        "maximum_pair_sum": max(valid_pairs) if valid_pairs else None
    }