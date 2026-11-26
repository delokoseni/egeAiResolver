
from itertools import combinations


def verify_sequence(numbers: list[int], specification) -> dict:
    if not numbers:
        raise ValueError("Последовательность пустая")

    # Независимо определяем делитель
    if (
        specification.pair_condition
        == "sum_divisible_by_minimum_positive_two_digit_number"
    ):
        candidates = [
            value for value in numbers
            if 10 <= value <= 99
        ]

    elif (
        specification.pair_condition
        == "absolute_difference_divisible_by_minimum_positive_multiple_of_35"
    ):
        candidates = [
            value for value in numbers
            if value > 0 and value % 35 == 0
        ]

    else:
        raise ValueError("Неизвестное условие для пары")

    if not candidates:
        raise ValueError("Не найдено число для определения делителя")

    divisor = min(candidates)

    valid_sums = []

    # Проверяем пары независимо от основного решателя
    for (i, first), (j, second) in combinations(
        enumerate(numbers), 2
    ):
        if specification.pair_definition == "adjacent":
            if j != i + 1:
                continue

        elif specification.pair_definition == "non_adjacent_distance_at_least_2":
            if j - i < 2:
                continue

        else:
            raise ValueError("Неизвестное определение пары")

        # Проверяем условие на элементы
        if (
            specification.element_condition
            == "exactly_one_positive_two_digit_number"
        ):
            first_is_two_digit = 10 <= first <= 99
            second_is_two_digit = 10 <= second <= 99

            if first_is_two_digit == second_is_two_digit:
                continue

        elif specification.element_condition == "elements_are_not_equal":
            if first == second:
                continue

        else:
            raise ValueError("Неизвестное условие на элементы")

        # Проверяем условие на пару
        if (
            specification.pair_condition
            == "sum_divisible_by_minimum_positive_two_digit_number"
        ):
            if (first + second) % divisor != 0:
                continue

        elif (
            specification.pair_condition
            == "absolute_difference_divisible_by_minimum_positive_multiple_of_35"
        ):
            if abs(first - second) % divisor != 0:
                continue

        valid_sums.append(first + second)

    return {
        "divisor": divisor,
        "pair_count": len(valid_sums),
        "maximum_pair_sum": max(valid_sums) if valid_sums else 0
    }
