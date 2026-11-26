from pathlib import Path

from graph import create_graph


def main():
    project_dir = Path(__file__).resolve().parent
    file_path = project_dir / "examples" / "17.txt"

    task_text = """
    Дана последовательность целых чисел.
    Рассматриваются пары элементов, расположенных на расстоянии
    не менее двух позиций друг от друга.

    Ровно один элемент пары должен быть положительным
    двузначным числом.

    Сумма элементов пары должна делиться без остатка
    на минимальное положительное двузначное число последовательности.

    Необходимо найти:
    1. Количество подходящих пар.
    2. Максимальную сумму элементов подходящей пары.
    """

    print("=" * 50)
    print("EGE AI SOLVER")
    print("=" * 50)

    # Создание и запуск графа
    app = create_graph()

    result = app.invoke({
        "task_text": task_text,
        "file_path": str(file_path)
    })

    specification = result["specification"]

    print("\nРезультат анализа:")
    print(specification.model_dump_json(indent=2))

    # Если Analyst отклонил задачу
    if not specification.supported:
        print("\nЗадача не поддерживается системой.")
        return

    solver_result = result["solver_result"]

    print("\nОписание алгоритма:")
    print(solver_result["algorithm_description"])

    print("\nУчебный Python-код:")
    print(solver_result["python_code"])

    print("\nПояснение:")
    print(solver_result["calculation_explanation"])

    print("\nРезультат вычислений:")
    print(solver_result["calculation"])

    review_result = result["review_result"]

    print("\nРезультат проверки:")
    print(f"Алгоритм корректен: {review_result['algorithm_correct']}")
    print(f"Код корректен: {review_result['code_correct']}")
    print(f"Вычисления корректны: {review_result['result_correct']}")

    print("\nНезависимый результат:")
    print(review_result["verified_calculation"])

    if review_result["issues"]:
        print("\nЗамечания:")
        for issue in review_result["issues"]:
            print(f"- {issue}")
    else:
        print("\nЗамечаний нет.")

    print("\nЗаключение Reviewer:")
    print(review_result["explanation"])

    print("\n" + "=" * 50)

    if review_result["approved"]:
        print("РЕШЕНИЕ ОДОБРЕНО")
    else:
        print("РЕШЕНИЕ НЕ ОДОБРЕНО")

    print("=" * 50)


if __name__ == "__main__":
    main()