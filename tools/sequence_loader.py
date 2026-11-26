
from pathlib import Path


def load_sequence(file_path: str) -> list[int]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Файл не найден: {path}"
        )

    text = path.read_text(encoding="utf-8")

    try:
        numbers = [int(value) for value in text.split()]
    except ValueError as error:
        raise ValueError(
            "Файл должен содержать только целые числа"
        ) from error

    if not numbers:
        raise ValueError("Последовательность пустая")

    return numbers
