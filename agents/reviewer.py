from pathlib import Path

from llm import llm
from schemas.review import ReviewResult
from tools.sequence_loader import load_sequence
from tools.solution_verifier import verify_sequence


class Reviewer:
    def __init__(self):
        project_dir = Path(__file__).resolve().parent.parent
        prompt_path = project_dir / "prompts" / "reviewer.txt"

        self.system_prompt = prompt_path.read_text(encoding="utf-8")

        self.structured_llm = llm.with_structured_output(
            ReviewResult,
            method="json_schema"
        )

    def review(
        self,
        task_text: str,
        specification,
        solver_result: dict,
        file_path: str
    ) -> dict:

        numbers = load_sequence(file_path)

        # Независимо пересчитываем результат
        verified_calculation = verify_sequence(numbers)

        # Сравниваем вычисления Solver и Reviewer
        solver_calculation = solver_result["calculation"]

        result_correct = (
            solver_calculation == verified_calculation
        )

        messages = [
            ("system", self.system_prompt),
            (
                "human",
                f"""
                Алгоритм Solver:
                {solver_result["algorithm_description"]}

                Python-код Solver:
                {solver_result["python_code"]}

                Результат Solver:
                {solver_calculation}

                Независимый результат:
                {verified_calculation}
                """
            )
        ]

        llm_review = self.structured_llm.invoke(messages)

        issues = list(llm_review.issues)

        if not result_correct:
            issues.append(
                "Результаты Solver и независимой проверки не совпадают."
            )

        approved = (
            llm_review.approved
            and llm_review.algorithm_correct
            and llm_review.code_correct
            and result_correct
        )

        return {
            "approved": approved,
            "algorithm_correct": llm_review.algorithm_correct,
            "code_correct": llm_review.code_correct,
            "result_correct": result_correct,
            "issues": issues,
            "explanation": llm_review.explanation,
            "verified_calculation": verified_calculation
        }