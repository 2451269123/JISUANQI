"""Streamlit web UI for the Python online calculator."""

from __future__ import annotations

import streamlit as st

from calculator_core import calculate_expression, format_number


BUTTON_ROWS = [
    ["AC", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "%", "+"],
    ["="],
]

BUTTON_VALUES = {
    "×": "*",
    "÷": "/",
}


def initialize_state() -> None:
    defaults = {
        "expression": "",
        "result": "",
        "history": [],
        "input_expression": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_expression_from_input() -> None:
    st.session_state.expression = st.session_state.input_expression


def append_to_expression(value: str) -> None:
    st.session_state.expression += BUTTON_VALUES.get(value, value)
    st.session_state.input_expression = st.session_state.expression


def backspace_expression() -> None:
    st.session_state.expression = st.session_state.expression[:-1]
    st.session_state.input_expression = st.session_state.expression


def clear_expression() -> None:
    st.session_state.expression = ""
    st.session_state.input_expression = ""
    st.session_state.result = ""


def calculate_current_expression() -> None:
    expression = st.session_state.expression.strip()
    if not expression:
        st.session_state.result = "表达式错误"
        return

    try:
        value = calculate_expression(expression)
        result = format_number(value)
    except ZeroDivisionError:
        st.session_state.result = "不能除以 0"
        return
    except ValueError:
        st.session_state.result = "表达式错误"
        return

    st.session_state.result = result
    st.session_state.history.insert(0, {"expression": expression, "result": result})
    st.session_state.history = st.session_state.history[:10]


def handle_button(label: str) -> None:
    if label == "AC":
        clear_expression()
    elif label == "⌫":
        backspace_expression()
    elif label == "=":
        calculate_current_expression()
    else:
        append_to_expression(label)


def render_buttons() -> None:
    for row in BUTTON_ROWS:
        columns = st.columns(len(row), gap="small")
        for column, label in zip(columns, row):
            button_type = "primary" if label == "=" else "secondary"
            column.button(
                label,
                use_container_width=True,
                type=button_type,
                on_click=handle_button,
                args=(label,),
            )


def render_history() -> None:
    st.sidebar.header("历史记录")
    if st.sidebar.button("清空历史记录", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    if not st.session_state.history:
        st.sidebar.caption("暂无历史记录")
        return

    for item in st.session_state.history:
        st.sidebar.markdown(f"`{item['expression']}` = **{item['result']}**")


def main() -> None:
    st.set_page_config(page_title="在线计算器", layout="wide")
    initialize_state()

    st.title("在线计算器")
    st.caption("使用 Python + Streamlit 实现，支持四则运算、括号、小数、百分号、负数和历史记录。")

    render_history()

    main_column, info_column = st.columns([2, 1], gap="large")

    with main_column:
        st.text_input(
            "数学表达式",
            key="input_expression",
            placeholder="例如：(1+2)*3 或 200*10%",
            on_change=sync_expression_from_input,
        )

        st.markdown(f"**当前表达式：** `{st.session_state.expression or ' '}`")
        result_text = st.session_state.result or "等待计算"
        st.markdown(
            f"""
            <div style="padding: 1rem; border-radius: 0.5rem; border: 1px solid #e5e7eb; background: #f9fafb;">
                <div style="font-size: 0.9rem; color: #6b7280;">计算结果</div>
                <div style="font-size: 2rem; font-weight: 700; color: #111827;">{result_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        render_buttons()

    with info_column:
        st.subheader("示例")
        examples = ["1+2*3", "(1+2)*3", "10/4", "50%", "200*10%", "-2+5", "5*-2", "0.1+0.2"]
        for example in examples:
            st.button(
                example,
                use_container_width=True,
                on_click=load_example,
                args=(example,),
            )


def load_example(example: str) -> None:
    st.session_state.expression = example
    st.session_state.input_expression = example
    calculate_current_expression()


if __name__ == "__main__":
    main()
