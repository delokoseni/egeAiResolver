
import streamlit as st
from pathlib import Path
import tempfile

from graph import create_graph


st.set_page_config(
    page_title="EGE AI Solver",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 EGE AI Solver")
st.caption(
    "Мультиагентная система автоматизированного решения "
    "задач №17 ЕГЭ по информатике"
)

st.divider()


# Ввод условия
st.subheader("Условие задачи")

default_task = """Дана последовательность целых чисел.
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

task_text = st.text_area(
    "Введите условие задачи",
    value=default_task,
    height=220
)


# Загрузка файла
st.subheader("Файл с последовательностью")

uploaded_file = st.file_uploader(
    "Загрузите TXT-файл",
    type=["txt"]
)


# Запуск
if st.button("Запустить решение", type="primary"):

    if not task_text.strip():
        st.error("Введите условие задачи.")
        st.stop()

    if uploaded_file is None:
        st.error("Загрузите файл с последовательностью.")
        st.stop()

    # Временный файл для передачи существующим агентам
    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=".txt",
        delete=False
    ) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        file_path = temp_file.name

    try:
        app = create_graph()

        with st.spinner("Мультиагентная система выполняет задачу..."):
            result = app.invoke({
                "task_text": task_text,
                "file_path": file_path
            })

        specification = result["specification"]

        st.divider()
        st.subheader("Результаты работы агентов")

        # ANALYST
        with st.expander("1. Analyst — анализ условия", expanded=True):
            if specification.supported:
                st.success("Задача поддерживается")
            else:
                st.error("Задача не поддерживается")

            st.json(specification.model_dump())

        if not specification.supported:
            st.warning(
                "Работа завершена: задача не поддерживается системой."
            )
            st.stop()

        solver_result = result["solver_result"]
        review_result = result["review_result"]

        # SOLVER
        with st.expander("2. Solver — решение задачи", expanded=True):
            st.markdown("**Описание алгоритма**")
            st.write(solver_result["algorithm_description"])

            st.markdown("**Учебный Python-код**")
            st.code(
                solver_result["python_code"],
                language="python"
            )

            st.markdown("**Пояснение**")
            st.write(solver_result["calculation_explanation"])

            st.markdown("**Результат вычислений**")
            st.json(solver_result["calculation"])

        # REVIEWER
        with st.expander("3. Reviewer — проверка решения", expanded=True):
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Алгоритм",
                "Корректен" if review_result["algorithm_correct"] else "Ошибка"
            )

            col2.metric(
                "Код",
                "Корректен" if review_result["code_correct"] else "Ошибка"
            )

            col3.metric(
                "Вычисления",
                "Корректны" if review_result["result_correct"] else "Ошибка"
            )

            st.markdown("**Независимый результат**")
            st.json(review_result["verified_calculation"])

            if review_result["issues"]:
                st.warning("Обнаружены замечания")
                for issue in review_result["issues"]:
                    st.write(f"- {issue}")
            else:
                st.success("Замечаний нет")

            st.markdown("**Заключение Reviewer**")
            st.write(review_result["explanation"])

        st.divider()

        # Итог
        if review_result["approved"]:
            st.success("РЕШЕНИЕ ОДОБРЕНО")

            calculation = solver_result["calculation"]

            col1, col2 = st.columns(2)

            col1.metric(
                "Количество подходящих пар",
                calculation["pair_count"]
            )

            col2.metric(
                "Максимальная сумма",
                calculation["maximum_pair_sum"]
            )
        else:
            st.error("РЕШЕНИЕ НЕ ОДОБРЕНО")

    except Exception as error:
        st.exception(error)

    finally:
        Path(file_path).unlink(missing_ok=True)
