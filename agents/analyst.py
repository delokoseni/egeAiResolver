from pathlib import Path

from llm import llm
from schemas.task import TaskSpecification

class Analyst:

    def __init__(self):
        project_dir = Path(__file__).resolve().parent.parent
        prompt_path = project_dir / "prompts" / "analyst.txt"

        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.structured_llm = llm.with_structured_output(
            TaskSpecification,
            method="json_schema"
        )

    def analyze(self, task_text: str, sequence_info: dict) -> TaskSpecification:

        if not task_text.strip():
            raise ValueError("Текст задачи не может быть пустым")

        if not sequence_info.get("file_provided"):
            raise ValueError("Файл с последовательностью не предоставлен")

        messages = [
            ("system", self.system_prompt),
            (
                "human",
                f"""
    Условие задачи:

    {task_text}

    Информация о входных данных:

    - Файл с последовательностью предоставлен: {sequence_info["file_provided"]}
    - Количество чисел в последовательности: {sequence_info["numbers_count"]}
    - Файл содержит только целые числа: {sequence_info["contains_integers"]}
    """
            )
        ]

        result = self.structured_llm.invoke(messages)

        return result
