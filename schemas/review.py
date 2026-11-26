from pydantic import BaseModel, Field

class ReviewResult(BaseModel):
    approved: bool = Field(
        description="Можно ли принять решение"
    )
    algorithm_correct: bool = Field(
        description="Корректна ли логика описанного алгоритма"
    )
    code_correct: bool = Field(
        description="Соответствует ли учебный Python-код условию задачи"
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Обнаруженные ошибки и замечания"
    )
    explanation: str = Field(
        description="Общее заключение Reviewer"
    )