
from pathlib import Path

from llm import llm
from schemas.task import TaskSpecification
from schemas.solution import SolverResult

from tools.sequence_loader import load_sequence
from tools.sequence_solver import solve_sequence


class Solver:

    def __init__(self):
        project_dir = Path(__file__).resolve().parent.parent

        prompt_path = project_dir / "prompts" / "solver.txt"

        self.system_prompt = prompt_path.read_text(
            encoding="utf-8"
        )

        self.structured_llm = llm.with_structured_output(
            SolverResult,
            method="json_schema"
        )

    def solve(
        self,
        task_text: str,
        specification: TaskSpecification,
        file_path: str
    ) -> dict:

        # Проверяем, что Analyst одобрил задачу
        if not specification.supported:
            raise ValueError(
                "Solver не может решать неподдерживаемую задачу"
            )

        # Дополнительная проверка спецификации
        if (
                specification.task_type != "pair_sequence_analysis"
                or specification.pair_definition == "unsupported"
                or specification.element_condition == "unsupported"
                or specification.pair_condition == "unsupported"
                or set(specification.required_outputs)
                != {"pair_count", "maximum_pair_sum"}
        ):
            raise ValueError(
                "Спецификация не соответствует поддерживаемому формату"
            )

        # Загружаем последовательность
        numbers = load_sequence(file_path)

        # Получаем описание алгоритма от LLM
        messages = [
            ("system", self.system_prompt),
            (
                "human",
                f"""
                Условие задачи:
                {task_text}

                Спецификация Analyst:
                {specification.model_dump_json(indent=2)}

                Количество чисел в файле: {len(numbers)}
                """
            )
        ]

        solver_result = self.structured_llm.invoke(messages)

        # Выполняем реальные вычисления обычным Python
        calculation = solve_sequence(numbers, specification)

        return {
            "algorithm_description": solver_result.algorithm_description,
            "python_code": solver_result.python_code,
            "calculation_explanation": solver_result.calculation_explanation,
            "calculation": calculation
        }
