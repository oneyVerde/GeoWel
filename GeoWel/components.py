import reflex as rx
from .styles import Button, Chart, Date, Text

# [Back] 이전 버튼
def back_button(on_click_handler):
    return rx.button(
        "← 이전",
        on_click=on_click_handler,
        **Button.btn_back_style
    )

# [F0, F1] f0, f1 버튼
def bar_chart_button(config: dict, on_click_event):
    return rx.button(
        config["title"],
        bg=config["bg_color"],
        on_click=on_click_event,
        **Button.btn_bar_chart_style
    )

# [F2] f2 버튼
def pie_chart_button():
    return rx.button(
        Text.F2,
        **Button.btn_pie_chart_style
    )

# [F0, F1] f0, f1 표
def table(data, columns) -> rx.Component:
    return rx.data_table(
        data=data,
        columns=columns,
        **Chart.TABLE
    )

# [Bar] bar chart 버튼을 감싸고 있는 box
def bar_chart_button_box(child_component: rx.Component) -> rx.Component:
    # child_component: rx.button
    return rx.box(
        child_component,
        **Chart.CHART_BUTTON_WRAPPER
    )

# [Pie] pie chart 버튼을 감싸고 있는 box
def pie_chart_button_box(child_component: rx.Component) -> rx.Component:
    # child_component: rx.button
    return rx.box(
        child_component,
        **Chart.CHART_BUTTON_WRAPPER
    )

# [Pie] fig 차트 하나를 받아서 그리는 함수
def render_pie_item(fig: dict) -> rx.Component:
    return rx.box(
        rx.plotly(
            data=fig,
            **Chart.PIE_PLOT
        ),
        **Chart.PIE_BOX
    )

# [Pie] 전체 그리드를 만드는 함수
def pie_chart_grid(data_state: list) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.foreach(
                data_state,
                render_pie_item
            ),
            **Chart.PIE_CHART_GRID
        ),
        **Chart.PIE_CHART_WRAPPER
    )

# [Table] 표를 감싸고 있는 box
def table_box(child_component: rx.Component, class_name: str) -> rx.Component:
    # child_component: rx.data_table
    return rx.box(
        child_component,
        class_name=class_name,
        **Chart.TABLE_WRAPPER
    )

# [Date] 버튼 및 발췌일자
def date_text(text: str) -> rx.Component:
    # content: 발췌일자 텍스트
    return rx.text(
        text,
        **Date.TEXT
    )