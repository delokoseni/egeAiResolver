from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from agents.analyst import Analyst
from agents.solver import Solver
from agents.reviewer import Reviewer

from tools.sequence_loader import load_sequence


# Общее состояние графа
class GraphState(TypedDict, total=False):
    task_text: str
    file_path: str
    sequence_info: dict

    specification: Any
    solver_result: dict
    review_result: dict


def create_graph():
    analyst = Analyst()
    solver = Solver()
    reviewer = Reviewer()

    # Узел 1: Analyst
    def analyst_node(state: GraphState):
        print("\n[1/3] ANALYST")
        print("Анализ условия задачи...")

        # Загружаем последовательность из файла
        numbers = load_sequence(state["file_path"])

        # Формируем метаданные входных данных
        sequence_info = {
            "file_provided": True,
            "numbers_count": len(numbers),
            "contains_integers": True
        }

        # Передаём Analyst условие задачи и информацию о файле
        specification = analyst.analyze(
            task_text=state["task_text"],
            sequence_info=sequence_info
        )

        return {
            "specification": specification,
            "sequence_info": sequence_info
        }

    # Узел 2: Solver
    def solver_node(state: GraphState):
        print("\n[2/3] SOLVER")
        print("Подготовка алгоритма и вычисление результата...")

        solver_result = solver.solve(
            task_text=state["task_text"],
            specification=state["specification"],
            file_path=state["file_path"]
        )

        return {
            "solver_result": solver_result
        }

    # Узел 3: Reviewer
    def reviewer_node(state: GraphState):
        print("\n[3/3] REVIEWER")
        print("Проверка решения...")

        review_result = reviewer.review(
            task_text=state["task_text"],
            specification=state["specification"],
            solver_result=state["solver_result"],
            file_path=state["file_path"]
        )

        return {
            "review_result": review_result
        }

    # Условный переход после Analyst
    def route_after_analyst(state: GraphState):
        if state["specification"].supported:
            return "solver"

        return "end"

    # Создание графа
    workflow = StateGraph(GraphState)

    workflow.add_node("analyst", analyst_node)
    workflow.add_node("solver", solver_node)
    workflow.add_node("reviewer", reviewer_node)

    workflow.add_edge(START, "analyst")

    workflow.add_conditional_edges(
        "analyst",
        route_after_analyst,
        {
            "solver": "solver",
            "end": END
        }
    )

    workflow.add_edge("solver", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()