import reflex as rx
from .styles import Button, Chart, Date, Text, Title, Map, Table, Color

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

# [F0, F1] main f0, f1 버튼
def main_bar_chart_button(config: dict, on_click_event):
    return rx.button(
        config["title"],
        bg=config["bg_color"],
        on_click=on_click_event,
        **Button.btn_main_bar_chart_style
    )

# [Text] 두줄 텍스트
def two_line_text(line1, line2):
    return rx.vstack(
        rx.text(
            line1,
            **Text.TWO_LINE_TEXT
        ),
        rx.text(
            line2,
            **Text.TWO_LINE_TEXT
        ),
        **Text.TWO_LINE_CONTAINER
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

# [Bar] bar chart를 감싸고 있는 box
def bar_chart_box(child_component: rx.Component) -> rx.Component:
    # child_component: rx.plotly
    return rx.box(
        child_component,
        **Chart.BAR_CHART_WRAPPER
    )

# [Table] 표를 감싸고 있는 box
def table_box(child_component: rx.Component, class_name: str) -> rx.Component:
    # child_component: rx.data_table
    return rx.box(
        child_component,
        class_name=class_name,
        **Chart.TABLE_WRAPPER
    )

# [F0, F1] f0, f1 표
def table(data, columns) -> rx.Component:
    return rx.data_table(
        data=data,
        columns=columns,
        **Chart.TABLE
    )

# [Bar] f0, f1 bar chart
def bar_chart(fig) -> rx.Component:
    return rx.plotly(
        data=fig,
        **Chart.BAR_CHART_PLOT
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

# [Date] 버튼 하단 발췌일자
def date_text(text: str) -> rx.Component:
    # content: 발췌일자 텍스트
    return rx.text(
        text,
        **Date.TEXT
    )

# [Text] 선택된 지역명
def region_name(region: str) -> rx.Component:
    # region: 지역명
    return rx.text(
        region,
        **Title.REGION
    )

# [Map] svg 지도
def map_cmp(data, on_click_handler):
    return rx.el.svg(
        rx.foreach(
            data,
            lambda item: rx.el.path(
                rx.el.title(item["name_kr"]),
                d=item["d"],
                fill=item["fill"],
                on_click=lambda: on_click_handler(item),
                **Map.MAP_PATH
            )
        ),
        **Map.MAP_CONTAINER
    )

# [Map] 지도 box
def map_box(child_component, mount):
    return rx.box(
        child_component,
        **Map.MAP_BOX_WRAPPER,
        on_mount=mount
    )

# [Main Table] 테이블 헤더
def render_table_header():
    # 대분류
    row1_cells = [
        rx.table.column_header_cell("구분", **Table.SECTION_CELL)
    ]
    for group in Table.HEADERS:
        row1_cells.append(
            rx.table.column_header_cell(
                group["title"],
                bg=group["bg"],
                col_span=len(group["columns"]),
                **Table.HEADER_CELL
            )
        )

    # 소분류
    row2_cells = []
    for group in Table.HEADERS:
        for col_name in group["columns"]:
            row2_cells.append(
                rx.table.column_header_cell(
                    col_name,
                    bg=group["bg"],
                    **Table.SUB_HEADER_CELL
                )
            )

    return rx.table.header(
        rx.table.row(*row1_cells),
        rx.table.row(*row2_cells)
    )

# [Main Table] 테이블 데이터
def render_main_row(row: dict):
    # 데이터 셀 생성
    row_text_color = rx.cond(
        row[Table.LABEL_COLUMN_KEY] == Table.HIGHLIGHT_KEYWORD,
        Color.MAP_MAIN,
        Color.BASIC_TEXT
    )

    cells = []
    # 1) 구분 셀
    cells.append(
        rx.table.cell(
            row[Table.LABEL_COLUMN_KEY],
            **Table.SECTION_LABEL_CELL
        )
    )

    # 2) 데이터 셀
    last_idx = len(Table.DATA_COLUMN_KEYS) - 1

    for idx, key in enumerate(Table.DATA_COLUMN_KEYS):
        cell_style = Table.DATA_CELL.copy()

        # 마지막 컬럼이면 우측 테두리 제거
        if idx == last_idx:
            cell_style["border_right"] = "none"

        cells.append(
            rx.table.cell(
                row[key],
                **cell_style
            )
        )

    return rx.table.row(
        *cells,
        color=row_text_color,
        **Table.ROW
    )

# [Main Table] 메인 테이블 컴포넌트
def main_data_table(data):
    return rx.box(
        rx.table.root(
            # 1) 헤더 렌더링
            render_table_header(),

            # 2) 바디 렌더링 (State 데이터 연결)
            rx.table.body(
                rx.foreach(
                    data,
                    render_main_row
                )
            ),
            width="100%",
            variant="surface",
        ),
        flex="1",
        overflow="auto",
        margin_left="0px"
    )
