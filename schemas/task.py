from typing import Literal

from pydantic import BaseModel, Field


class TaskSpecification(BaseModel):
    supported: bool = Field(
        description="Поддерживается ли задача нашей системой"
    )

    task_type: Literal[
        "pair_sequence_analysis",
        "unsupported"
    ] = Field(
        description="Тип задачи"
    )

    pair_definition: str = Field(
        default="",
        description="Определение пары элементов. Если задача не поддерживается, пустая строка"
    )

    element_condition: Literal[
        "exactly_one_positive_two_digit_number",
        "unsupported"
    ] = Field(
        description="Условие на отдельные элементы пары"
    )

    pair_condition: Literal[
        "sum_divisible_by_minimum_positive_two_digit_number",
        "unsupported"
    ] = Field(
        description="Условие, которому должна удовлетворять пара"
    )

    required_outputs: list[
        Literal["pair_count", "maximum_pair_sum"]
    ] = Field(
        default_factory=list,
        description="Требуемые результаты"
    )

    explanation: str = Field(
        default="",
        description="Объяснение результата анализа"
    )

    unsupported_reason: str | None = Field(
        default=None,
        description="Причина неподдерживаемого типа задачи"
    )
