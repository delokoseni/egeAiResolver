
def is_positive_two_digit(number: int) -> bool:
    return 10 <= number <= 99


def solve_sequence(numbers: list[int], specification) -> dict:
    if not numbers:
        raise ValueError("Последовательность пустая")

    # Выбираем числа, из которых определяется делитель
    if (
        specification.pair_condition
        == "sum_divisible_by_minimum_positive_two_digit_number"
    ):
        special_numbers = [
            number for number in numbers
            if is_positive_two_digit(number)
        ]

    elif (
        specification.pair_condition
        == "absolute_difference_divisible_by_minimum_positive_multiple_of_35"
    ):
        special_numbers = [
            number for number in numbers
            if number > 0 and number % 35 == 0
        ]

    else:
        raise ValueError("Неизвестное условие для пары")

    if not special_numbers:
        raise ValueError(
            "В последовательности нет числа для определения делителя"
        )

    divisor = min(special_numbers)

    pair_count = 0
    maximum_pair_sum = None

    # Перебираем первые элементы пар
    for i in range(len(numbers) - 1):

        # Для соседних пар рассматриваем только следующий элемент.
        # Для несоседних — все элементы начиная через одну позицию.
        if specification.pair_definition == "adjacent":
            candidate_indices = (i + 1,)

        elif (
            specification.pair_definition
            == "non_adjacent_distance_at_least_2"
        ):
            candidate_indices = range(i + 2, len(numbers))

        else:
            raise ValueError("Неизвестное определение пары")

        for j in candidate_indices:
            first = numbers[i]
            second = numbers[j]

            # Проверяем условие на элементы
            if (
                specification.element_condition
                == "exactly_one_positive_two_digit_number"
            ):
                condition = (
                    is_positive_two_digit(first)
                    != is_positive_two_digit(second)
                )

            elif (
                specification.element_condition
                == "elements_are_not_equal"
            ):
                condition = first != second

            else:
                raise ValueError("Неизвестное условие на элементы")

            if not condition:
                continue

            # Проверяем математическое условие пары
            if (
                specification.pair_condition
                == "sum_divisible_by_minimum_positive_two_digit_number"
            ):
                pair_condition = (first + second) % divisor == 0

            elif (
                specification.pair_condition
                == "absolute_difference_divisible_by_minimum_positive_multiple_of_35"
            ):
                pair_condition = abs(first - second) % divisor == 0

            else:
                raise ValueError("Неизвестное условие для пары")

            if not pair_condition:
                continue

            pair_sum = first + second
            pair_count += 1

            if (
                maximum_pair_sum is None
                or pair_sum > maximum_pair_sum
            ):
                maximum_pair_sum = pair_sum

    return {
        "divisor": divisor,
        "pair_count": pair_count,
        "maximum_pair_sum": (
            maximum_pair_sum if maximum_pair_sum is not None else 0
        )
    }
