import reflex as rx
from .state import State

def index() -> rx.Component:
    return rx.hstack(
        # =========================================================
        # [왼쪽 패널] 지도 공간 (40%)
        # =========================================================
        rx.box(
            rx.vstack(
                rx.heading("지역별 통합돌봄 사업 현황", size="7", padding_top="30px"),
                        rx.text(
                            State.selected_region_kr,
                            size="6",
                            font_weight="bold",
                            color="black",
                            padding_top="20px",
                            padding_bottom="10px"
                        ),
                        rx.el.svg(
                            rx.foreach(
                                State.map_paths,
                                lambda item: rx.el.path(
                                    rx.el.title(item["name_kr"]),
                                    d=item["d"],
                                    fill=item["fill"],
                                    stroke="white",
                                    stroke_width="1",
                                    on_click=lambda: State.handle_map_click(item),
                                    _hover={
                                        "fill": "#787878",
                                        "cursor": "pointer",
                                        "stroke": "black"
                                    },
                                    transition="all 0.2s ease"
                                )
                            ),
                            viewBox="-1500 -1000 5000 3000",
                            width="100%",
                            height="100vh",
                            preserveAspectRatio="xMidYMid meet",
                            padding_left="100px",
                            padding_top="80px"
                        ),
                width="100%",
                height="100%",
                align_items="center",
                spacing="5",
            ),
            width="40%",
            height="100vh",
            bg="#ffffff",
            border_right="1px solid #e0e0e0",
            overflow="hidden",
            position="relative",
            z_index="999",

            on_mount=State.load_map_data
        ),

        # =========================================================
        # [오른쪽 패널] 나머지 공간 (60%)
        # =========================================================
        rx.box(
            # 1. 지역 선택 여부 확인
            rx.cond(
                State.selected_region_kr != "",

                # [Case A] 지역이 선택되었을 때
                rx.cond(
                    State.current_view == "main",

                    # -------------------------------------------------
                    # [View 1] 메인 화면: F0, F1, F2 행별 배치
                    # -------------------------------------------------
                    rx.vstack(
                        rx.heading(f"{State.selected_region_kr} 통합돌봄 현황", size="5", padding_top="10px"),

                        # --- [Row 1] F0 영역 ---
                        rx.vstack(
                            rx.hstack(
                                # 왼쪽: 버튼
                                rx.box(
                                    rx.button(
                                        "신청 및 연계 현황",
                                        font_size="17px",
                                        on_click=State.toggle_f0_chart,
                                        width="100%",
                                        height="55px",
                                        bg="#d7f0bd",  # f0 버튼
                                        margin_top="15px",
                                        margin_left="15px",
                                        color="#333333",
                                        font_weight="bold",
                                        transition="all 0.2s ease-in-out",
                                        _active={
                                            "transform": "translateY(1px)"
                                        },
                                        _hover={
                                            "transform": "scale(1.05)",
                                            "color": "black",
                                        },
                                    ),
                                    width="20%",
                                    min_width="200px",
                                    margin_right="13px"
                                ),
                                # 오른쪽: 표
                                rx.box(
                                    rx.data_table(data=State.f0_table_data, columns=State.f0_columns, size="1"),
                                    flex="1",
                                    overflow="auto",
                                    margin_top="10px",
                                    margin_right="15px",
                                    class_name="f0-table",
                                ),
                                width="100%",
                                align_items="start"
                            ),
                            rx.text(
                                "* 발췌일자: 1) 2026.1.12. / 예산지원형: 2025.2.17.~2026.1.9., 기술지원형: 2025.7.14~2026.1.9. 접수일 기준",
                                font_size="16px",
                                color="#333333",
                                margin_top="-10px",
                                text_align="left",
                                width="100%",
                                font_weight="bold",
                                padding_left="5px",
                                margin_left="10px"
                            ),
                            width="100%",
                            height="100%",
                            border="1px solid #eee",
                            padding="1",
                            border_radius="5px"
                        ),
                        # --- [Row 2] F1 영역 ---
                        rx.vstack(
                            rx.hstack(
                                # 왼쪽: 버튼
                                rx.box(
                                    rx.button(
                                        "퇴원 환자 지원 현황",
                                        font_size="17px",
                                        on_click=State.toggle_f1_chart,
                                        width="100%",
                                        height="55px",
                                        bg="#ffd3a7",  # f1 버튼
                                        margin_top="15px",
                                        margin_left="15px",
                                        color="#333333",
                                        font_weight="bold",
                                        transition="all 0.2s ease-in-out",
                                        _active={
                                            "transform": "translateY(1px)"
                                        },
                                        _hover={
                                            "transform": "scale(1.05)",
                                            "color": "black",
                                        },
                                    ),
                                    width="20%",
                                    min_width="200px",
                                    margin_right="13px"
                                ),
                                # 오른쪽: 표
                                rx.box(
                                    rx.data_table(data=State.f1_table_data, columns=State.f1_columns, size="1"),
                                    flex="1",
                                    overflow="auto",
                                    margin_top="10px",
                                    margin_right="15px",
                                    class_name="f0-table",
                                ),
                                width="100%",
                                align_items="start"
                            ),
                            rx.text(
                                "* 발췌일자: 2025.12.31.",
                                font_size="16px",
                                color="#333333",
                                margin_top="-10px",
                                text_align="left",
                                width="100%",
                                font_weight="bold",
                                padding_left="5px",
                                margin_left="10px"
                            ),
                            width="100%",
                            height="100%",
                            border="1px solid #eee",
                            padding="1",
                            border_radius="5px"
                        ),

                        # --- [Row 3] F2 영역 ---
                        rx.vstack(
                            # 위쪽: 버튼
                            rx.button(
                                "자원 현황", # f2 버튼
                                font_size="17px",
                                width="20%",
                                height="50px",
                                bg="#fff5b1",

                                color="#333333",
                                font_weight="bold",

                                cursor="default",
                                disabled=True,
                                _hover={"bg": "#fff5b1"},
                                _active={"bg": "#fff5b1"},
                                margin_left="15px",
                                margin_top="10px"
                            ),

                            rx.box(
                                rx.text(
                                    "* 발췌일자: 2025.12.1.",
                                    font_size="16px",
                                    color="#1B1B1B",
                                    font_weight="bold"
                                ),
                                width="100%",
                                text_align="left",
                                padding_left="20px",
                                margin_top="10px"
                            ),

                            # 오른쪽: 파이차트
                            rx.box(
                                rx.flex(
                                    rx.foreach(
                                        State.f2_pie_figs,
                                        lambda fig: rx.box(
                                            rx.plotly(data=fig, config={"displayModeBar": False}, use_resize_handler=True),
                                            width="320px", min_width="320px", height="300px",
                                            margin="0px", overflow="hidden"
                                        )
                                    ),
                                    wrap="wrap",
                                    spacing="0",
                                    justify="center",
                                ),

                                flex="1",
                                overflow="auto"
                            ),
                            width="100%",
                            border="1px solid #eee", padding="2", border_radius="5px", spacing="0"
                        ),
                        spacing="2",
                        width="100%",
                        height="100%",
                        overflow_y="auto",
                        padding="10px"
                    ),

                    # -------------------------------------------------
                    # [View 2 & 3] 상세 차트 화면 (F0 또는 F1)
                    # -------------------------------------------------
                    rx.cond(
                        State.current_view == "f0",

                        # [View 2] F0 Bar Chart 화면
                        rx.vstack(
                            rx.hstack(
                                rx.button("← 이전", on_click=State.toggle_f0_chart, color_scheme="gray", variant="outline", color="#333333", font_weight="bold"),
                                align_items="center",
                                width="100%",
                                padding="20px"
                            ),
                            rx.box(
                                rx.plotly(
                                    data=State.f0_bar_fig,
                                    use_resize_handler=True,
                                    width="100%",
                                    height="600px"
                                ),
                                width="100%",
                                padding="10px",
                                flex="1",
                                style={
                                    "zoom": "0.95"
                                }
                            ),
                            width="100%",
                            height="100%"
                        ),

                        # [View 3] F1 Bar Chart 화면 (else: current_view == "f1")
                        rx.vstack(
                            rx.hstack(
                                rx.button("← 이전", on_click=State.toggle_f1_chart, color_scheme="gray", variant="outline", color="#333333", font_weight="bold"),
                                align_items="center",
                                width="100%",
                                padding="20px"
                            ),
                            rx.center(
                                rx.plotly(
                                    data=State.f1_bar_fig,
                                    use_resize_handler=True,
                                    width="100%",
                                    height="600px"
                                ),
                                width="100%",
                                padding="10px",
                                flex="1"
                            ),

                            width="100%",
                            height="100%"
                        )
                    )
                ),
                rx.cond(
                    State.current_view == "main",

                    # =========================================================
                    # [View 1] 전국 메인 화면: 버튼(좌) + 테이블(우)
                    # =========================================================
                    rx.vstack(
                        rx.heading(
                            "전국 통합돌봄 현황", size="6", margin_bottom="10px", text_align="center",
                                   font_weight="bold"),

                        # [핵심 수정] 가로 배치 (버튼 스택 + 테이블 박스)
                        rx.hstack(
                            # 1. 왼쪽: 버튼 메뉴 (F0, F1, F2)
                            rx.vstack(
                                # (F0) 신청 및 연계 현황 (줄바꿈 적용됨)
                                rx.button(
                                    rx.vstack(
                                        rx.text("신청 및", font_size="14px", font_weight="bold", line_height="1.2"),
                                        rx.text("연계 현황", font_size="14px", font_weight="bold", line_height="1.2"),
                                        spacing="0",
                                        align_items="center",
                                        justify="center",
                                        width="100%"
                                    ),
                                    on_click=State.toggle_f0_chart,
                                    width="90%",
                                    height="55px",
                                    bg="#d7f0bd",
                                    color="#333333",
                                    transition="all 0.2s ease-in-out",
                                    _active={"transform": "translateY(1px)"},
                                    _hover={"transform": "scale(1.05)", "color": "black"},
                                ),

                                # (F2) 자원 현황
                                rx.button(
                                    "자원 현황",
                                    font_size="14px",
                                    on_click=State.toggle_f2_chart,
                                    width="90%",
                                    height="55px",
                                    bg="#fff5b1",
                                    color="#333333",
                                    font_weight="bold",
                                    _active={"transform": "translateY(1px)"},
                                    _hover={"transform": "scale(1.05)", "color": "black"},
                                ),

                                # (F1) 퇴원 환자 지원 현황
                                rx.button(
                                    rx.text("퇴원 환자 지원 현황", line_height="1.2", font_size="14px", font_weight="bold"),
                                    on_click=State.toggle_f1_chart,
                                    width="90%",
                                    height="55px",
                                    bg="#ffd3a7",
                                    color="#333333",
                                    font_weight="bold",
                                    transition="all 0.2s ease-in-out",
                                    _active={"transform": "translateY(1px)"},
                                    _hover={"transform": "scale(1.05)", "color": "black"},
                                ),

                                width="100px",
                                spacing="3",
                                padding_top="0px"
                            ),

                            # 2. 오른쪽: 테이블 (남은 공간 차지)
                            rx.box(
                                rx.table.root(
                                    rx.table.header(
                                        # [Row 1] 대분류
                                        rx.table.row(
                                            rx.table.column_header_cell("구분", row_span=2, vertical_align="middle",
                                                                        text_align="center", bg="#e9e9e9",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("1) 신청 및 연계 현황(명)", vertical_align="middle",
                                                                        col_span=3, text_align="center",
                                                                        bg="#d7f0bd", border_bottom="2px solid #ffffff",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("2) 자원 현황(건)", vertical_align="middle",
                                                                        col_span=5, text_align="center",
                                                                        bg="#fff5b1", border_bottom="2px solid #ffffff",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("3) 퇴원환자 지원 현황(개, %, 건)",
                                                                        vertical_align="middle", col_span=3,
                                                                        text_align="center",
                                                                        bg="#ffd3a7",
                                                                        border_bottom="2px solid #ffffff"),
                                        ),
                                        # [Row 2] 소분류
                                        rx.table.row(
                                            # 신청 하위
                                            rx.table.column_header_cell("신청자", vertical_align="middle", bg="#d7f0bd",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("통합판정완료", vertical_align="middle", bg="#d7f0bd",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("서비스연계", vertical_align="middle", bg="#d7f0bd",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            # 자원 하위
                                            rx.table.column_header_cell("보건의료", vertical_align="middle", bg="#fff5b1",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("장기요양", vertical_align="middle", bg="#fff5b1",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("생활지원", vertical_align="middle", bg="#fff5b1",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("주거지원", vertical_align="middle", bg="#fff5b1",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("자체사업", vertical_align="middle", bg="#fff5b1",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            # 퇴원환자 하위
                                            rx.table.column_header_cell("요양병원수", vertical_align="middle", bg="#ffd3a7",
                                                                        text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("관외환자 입원율", vertical_align="middle",
                                                                        bg="#ffd3a7", text_align="center",
                                                                        font_size="0.9em",
                                                                        border_right="2px solid #ffffff"),
                                            rx.table.column_header_cell("자원연계건수", vertical_align="middle", bg="#ffd3a7",
                                                                        text_align="center",
                                                                        font_size="0.9em"),
                                        ),
                                    ),

                                    rx.table.body(
                                        rx.foreach(
                                            State.main_data,
                                            render_main_row
                                        )
                                    ),
                                    width="100%",
                                    variant="surface",
                                ),
                                flex="1",
                                overflow="auto",
                                margin_left="0px"  # [수정] 테이블 왼쪽 여백 제거
                            ),
                            width="100%",
                            align_items="start",
                            spacing="1"  # [수정] 버튼과 테이블 사이 간격 1
                        ),
                        # main 발췌일자
                        rx.vstack(
                            rx.hstack(
                                rx.text("※ 발췌일자", margin_left="20px", as_="span"),
                                rx.text(
                                    "1) 2026.1.12.", rx.el.sup("*"), margin_left="20px", as_="span"),
                                rx.text("2) 2025.12.1.", margin_left="20px", as_="span"),
                                rx.text("3) 2025.12.31.", margin_left="20px", as_="span"),
                                font_size="16px",
                                color="#333333",
                                margin_top="5px",
                                width="100%",
                                text_align="left",
                                font_weight="bold"
                            ),
                            rx.text("* 예산지원형: 2025.2.17.~2026.1.9., 기술지원형: 2025.7.14~2026.1.9. 접수일 기준",
                                    font_size="14px",
                                    color="#333333",
                                    margin_top="10px",
                                    margin_left="130px",
                                    width="100%",
                                    text_align="left",
                                    font_weight="bold",
                                    as_="span"
                            ),
                            spacing="0"
                        ),
                        width="100%",
                        height="100%",
                        padding="20px",
                        align_items="stretch"
                    ),

                    # =========================================================
                    # [View 2 & 3] 상세 차트 화면 (F0 또는 F1)
                    # =========================================================
                    rx.cond(
                        State.current_view == "f0",

                        # [View 2] F0 Bar Chart 화면 (신청 및 연계)
                        rx.vstack(
                            rx.hstack(
                                rx.button("← 이전", on_click=State.toggle_f0_chart, color_scheme="gray",
                                          variant="outline",
                                          color="#333333", font_weight="bold"),
                                align_items="center",
                                width="100%",
                                padding="20px"
                            ),
                            rx.box(
                                rx.plotly(
                                    data=State.f0_bar_fig,
                                    use_resize_handler=True,
                                    width="100%",
                                    height="600px"
                                ),
                                width="100%",
                                padding="10px",
                                flex="1",
                                style={
                                    "zoom": "0.95"
                                }
                            ),
                            width="100%",
                            height="100%"
                        ),
                        rx.cond(
                            # [View 3] F1 Bar Chart 화면 (퇴원 환자 지원)
                            State.current_view == "f1",
                            rx.vstack(
                                rx.hstack(
                                    rx.button("← 이전", on_click=State.toggle_f1_chart, color_scheme="gray",
                                              variant="outline",
                                              color="#333333", font_weight="bold"),
                                    align_items="center",
                                    width="100%",
                                    padding="20px"
                                ),
                                rx.center(
                                    rx.plotly(
                                        data=State.f1_bar_fig,
                                        use_resize_handler=True,
                                        width="100%",
                                        height="600px"
                                    ),
                                    width="100%",
                                    padding="10px",
                                    flex="1"
                                ),
                                width="100%",
                                height="100%"
                            ),
                            # [View 4] F2 Pie Chart 화면 (자원 현황)
                            rx.vstack(
                                # 1. 상단: 뒤로가기 버튼
                                rx.box(
                                    rx.button(
                                        "← 이전",
                                        on_click=State.toggle_f2_chart,
                                        color_scheme="gray",
                                        variant="outline",
                                        color="#333333",
                                        font_weight="bold",
                                        margin_bottom="70px"
                                    ),
                                    align_items="left",
                                    width="100%",
                                    padding="20px"
                                ),
                                # 2. 메인 콘텐츠: 파이차트 및 하단 정보 (Box)
                                rx.box(
                                    # (1) 파이차트 나열 (Flex)
                                    rx.flex(
                                        rx.foreach(
                                            State.f2_pie_figs,
                                            lambda fig: rx.box(
                                                rx.plotly(
                                                    data=fig,
                                                    config={"displayModeBar": False},
                                                    use_resize_handler=True
                                                ),
                                                width="320px",
                                                min_width="320px",
                                                height="300px",
                                                margin="5px",
                                                overflow="hidden"
                                            )
                                        ),
                                        wrap="wrap",
                                        spacing="4",
                                        justify="center",
                                        width="100%"
                                    ),
                                    width="100%",
                                    padding="10px",
                                    overflow_y="auto"
                                ),
                                rx.box(
                                    rx.text(
                                        f"* 발췌일자: 2025.12.1.",
                                        font_size="16px",
                                        color="#1B1B1B",
                                        font_weight="bold",
                                        text_align="left",
                                    ),
                                    width="100%",
                                    padding="20px",
                                    padding_top="10px"
                                ),
                                width="100%",
                                height="100%",
                                style={
                                    "zoom": "0.978",  # Chrome, Edge 등에서 90% 축소 효과
                                }
                            )
                        ),

                    )
                )
                # ==
            ),
            align_items="center",
            width="60%",
            height="100vh",
            overflow="flex",
            z_index="1"
        ),

        width="100%",
        spacing="0"
    )

# main table
def render_main_row(row: dict):
    row_border_style = "1.5px solid #E2E2E2"
    highlight_row = "전국"
    text_color = rx.cond(
        row["구분_Unnamed: 0_level_1"] == highlight_row,
        "#0069e3",
        "#333333"
    )
    return rx.table.row(
        # 1. 구분
        rx.table.cell(row["구분_Unnamed: 0_level_1"], text_align="center", border_right=row_border_style),

        # 2. 신청 및 연계 현황
        rx.table.cell(row["신청 및 연계 현황 (명)_신청자"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["신청 및 연계 현황 (명)_통합판정완료"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["신청 및 연계 현황 (명)_서비스연계"], text_align="right", border_right=row_border_style),

        # 3. 자원 현황
        rx.table.cell(row["자원 현황 (건)_보건의료"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["자원 현황 (건)_장기요양"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["자원 현황 (건)_생활지원"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["자원 현황 (건)_주거지원"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["자원 현황 (건)_자체사업"], text_align="right", border_right=row_border_style),

        # 4. 퇴원환자 지원 현황
        rx.table.cell(row["퇴원환자 지원 현황 (개, %, 건)_요양병원수"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["퇴원환자 지원 현황 (개, %, 건)_관외환자 입원율"], text_align="right", border_right=row_border_style),
        rx.table.cell(row["퇴원환자 지원 현황 (개, %, 건)_자원연계건수"], text_align="right"),

        height="37px",
        align="center",
        _hover={"bg": "#f5f5f5"},
        color=text_color
    )

global_style = {
    "th": {
        "font_size": "13px !important",
        "padding": "4px !important",
        "text_align": "center !important",
        #"background_color": "#b0b0b0 !important",
        "color" : "#000000 !important"
    },
    # 2. 테이블 데이터 칸 (Cell)
    "td": {
        "font_size": "14px !important",
        "padding": "2px 4px !important",
        "height": "auto !important",
        "text_align": "center !important",
        "font_weight": "bold !important",
    },
    ".f0-table th": {
            "background_color": "#d1e0fc !important",
            "border": "2px solid #ffffff !important",
    },
    ".f1-table th": {
            "background_color": "#d1e0fc !important",
            "border": "2px solid #ffffff !important",
    },
    ".f0-table thead tr:first-child th:first-child": {
        "border_top_left_radius": "10px !important",
    },
    ".f0-table thead tr:first-child th:last-child": {
        "border_top_right_radius": "10px !important",
    },
    ".f1-table thead tr:first-child th:first-child": {
        "border_top_left_radius": "10px !important",
    },
    ".f1-table thead tr:first-child th:last-child": {
        "border_top_right_radius": "10px !important",
    }
}

app = rx.App(style=global_style)
app.add_page(index, on_load=State.load_excel_data)