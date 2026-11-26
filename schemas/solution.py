from pydantic import BaseModel, Field


class SolverResult(BaseModel):
    algorithm_description: str = Field(
        description="Описание алгоритма решения задачи"
    )
    python_code: str = Field(
        description="Учебный Python-код решения задачи"
    )
    calculation_explanation: str = Field(
        description="Объяснение математической логики решения"
    )