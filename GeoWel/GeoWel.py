import reflex as rx
from .state import State
from .styles import Text
from .configuration import Config
from . import components as CMP

def index() -> rx.Component:
    return rx.hstack(
        # =========================================================
        # [왼쪽 패널] 지도 공간 (40%)
        # =========================================================
        CMP.map_box(
            rx.vstack(
                rx.heading("지역별 통합돌봄 사업 현황", size="7", padding_top="30px"),
                        CMP.region_name(
                            State.selected_region_kr
                        ),
                        CMP.map_cmp(
                            State.map_paths,
                            State.handle_map_click
                        ),
                width="100%",
                height="100%",
                align_items="center",
                spacing="5",
            ),
            State.load_map_data
        ),

        # =========================================================
        # [오른쪽 패널] 대시보드 공간 (60%)
        # =========================================================
        rx.box(
            # [Logic] 지역 선택 여부
            rx.cond(
                State.selected_region_kr != "",

                # [Case A] 지역이 선택되었을 때
                rx.cond(
                    State.current_view == "main",

                    # -------------------------------------------------
                    # [View 1] 지역: F0, F1, F2 행별 배치
                    # -------------------------------------------------
                    rx.vstack(
                        rx.heading(f"{State.selected_region_kr} 통합돌봄 현황", size="5", padding_top="10px"),

                        # [Row 1] F0 영역 (신청 및 연계)
                        rx.vstack(
                            rx.hstack(
                                # F0 차트 버튼
                                CMP.bar_chart_button_box(
                                    CMP.bar_chart_button(
                                        Config.F0_CONFIG,
                                        State.toggle_f0_chart
                                    )
                                ),
                                # F0 데이터 테이블
                                CMP.table_box(
                                    CMP.table(
                                        data=State.f0_table_data,
                                        columns=State.f0_columns
                                    ),
                                    class_name="f0-table"
                                ),
                                width="100%",
                                align_items="start"
                            ),
                            CMP.date_text(
                                Text.F0_DATE
                            ),
                            width="100%",
                            height="100%",
                            border="1px solid #eee",
                            padding="1",
                            border_radius="5px"
                        ),
                        # [Row 2] F1 영역 (퇴원환자 지원)
                        rx.vstack(
                            rx.hstack(
                                # F1 차트 버튼
                                CMP.bar_chart_button_box(
                                    CMP.bar_chart_button(
                                        Config.F1_CONFIG,
                                        State.toggle_f1_chart
                                    )
                                ),
                                # F1 데이터 테이블
                                CMP.table_box(
                                    CMP.table(
                                        data=State.f1_table_data,
                                        columns=State.f1_columns
                                    ),
                                    class_name="f1-table"
                                ),
                                width="100%",
                                align_items="start"
                            ),
                            CMP.date_text(
                                Text.F1_DATE
                            ),
                            width="100%",
                            height="100%",
                            border="1px solid #eee",
                            padding="1",
                            border_radius="5px"
                        ),

                        # [Row 3] F2 영역 (자원 현황)
                        rx.vstack(
                            # F2 차트 버튼
                            CMP.pie_chart_button_box(
                                CMP.pie_chart_button()
                            ),

                            # F2 파이 차트
                            CMP.pie_chart_grid(
                                State.f2_pie_figs
                            ),
                            width="100%",
                            border="1px solid #eee", padding="2", border_radius="5px", spacing="0"
                        ),
                        width="100%",
                        height="auto",
                        overflow_y="auto",
                        padding="10px"
                    ),

                    # -------------------------------------------------
                    # [View 2 & 3] 상세 차트 화면 (F0, F1)
                    # -------------------------------------------------
                    rx.cond(
                        State.current_view == "f0",

                        # [View 2] F0 상세 차트 (Bar)
                        rx.vstack(
                            CMP.back_button(
                                State.toggle_f0_chart
                            ),
                            CMP.bar_chart_box(
                                CMP.bar_chart(
                                    State.f0_bar_fig
                                )
                            ),
                            width="100%",
                            height="100%",
                            spacing="0"
                        ),

                        # [View 3] F1 상세 차트 (Bar)
                        rx.vstack(
                            CMP.back_button(
                              State.toggle_f1_chart
                            ),
                            CMP.bar_chart_box(
                                CMP.bar_chart(
                                    State.f1_bar_fig
                                )
                            ),
                            width="100%",
                            height="100%",
                            spacing="0"
                        )
                    )
                ),
                # [Case B] 지역이 선택되지 않았을 때 (전국)
                rx.cond(
                    State.current_view == "main",

                    # =========================================================
                    # [View 1] 전국 메인: 버튼 + 메인 테이블
                    # =========================================================
                    rx.vstack(
                        rx.heading(
                            "전국 통합돌봄 현황", size="6", margin_bottom="10px", text_align="center",
                                   font_weight="bold"),

                        rx.hstack(
                            # [Column 1] 메뉴 버튼 그룹
                            rx.vstack(
                                # F0 차트 버튼 (신청 및 연계)
                                CMP.main_bar_chart_button(
                                    Config.MAIN_F0_CONFIG,
                                    State.toggle_f0_chart
                                ),
                                # F2 차트 버튼 (자원 현황)
                                CMP.main_bar_chart_button(
                                    Config.F2_CONFIG,
                                    State.toggle_f2_chart
                                ),
                                # F1 차트 버튼 (퇴원환자 지원)
                                CMP.main_bar_chart_button(
                                    Config.F1_CONFIG,
                                    State.toggle_f1_chart
                                ),
                                width="100px",
                                spacing="3",
                                padding_top="0px"
                            ),

                            # [Column 2] 전국 데이터 테이블
                            CMP.main_data_table(
                                State.main_table_data
                            ),
                            width="100%",
                            align_items="start",
                            spacing="1"
                        ),
                        # [Footer] 메인 테이블 발췌일자
                        CMP.main_table_date(),
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

                        # [View 2] F0 상세 차트 (Bar)
                        rx.vstack(
                            CMP.back_button(
                                State.toggle_f0_chart
                            ),
                            CMP.bar_chart_box(
                                CMP.bar_chart(
                                    State.f0_bar_fig
                                )
                            ),
                            width="100%",
                            height="100%"
                        ),
                        rx.cond(
                            # [View 3] F1 상세 차트 (Bar)
                            State.current_view == "f1",
                            rx.vstack(
                                CMP.back_button(
                                    State.toggle_f1_chart
                                ),
                                CMP.bar_chart_box(
                                    CMP.bar_chart(
                                        State.f1_bar_fig
                                    )
                                ),
                                width="100%",
                                height="100%"
                            ),
                            # [View 4] F2 상세 차트 (Pie)
                            rx.vstack(
                                CMP.back_button(
                                    State.toggle_f2_chart
                                ),
                                CMP.pie_chart_grid(
                                    State.f2_pie_figs
                                ),
                                rx.box(
                                    CMP.date_text(
                                        Text.F2_DATE
                                    ),
                                    margin_top="-200px"
                                ),
                                width="100%",
                                height="100%",
                                spacing="0",
                                style={
                                    "zoom": "0.978",
                                },
                                padding="20px"
                            )
                        ),
                    )
                )
            ),
            align_items="center",
            width="60%", # 대시보드 화면 비율
            height="100vh",
            overflow="flex",
            z_index="1"
        ),

        width="100%",
        spacing="0"
    )

global_style = {
# 1. 테이블 헤더 (Th)
    "th": {
        "font_size": "13px !important",
        "padding": "4px !important",
        "text_align": "center !important",
        "color" : "#000000 !important"
    },
    # 2. 테이블 데이터 칸 (Td)
    "td": {
        "font_size": "14px !important",
        "padding": "2px 4px !important",
        "height": "auto !important",
        "text_align": "center !important",
        "font_weight": "bold !important",
    },
    # 3. F0/F1 테이블 별도 스타일
    ".f0-table th": {
            "background_color": "#d1e0fc !important",
            "border": "2px solid #ffffff !important",
    },
    ".f1-table th": {
            "background_color": "#d1e0fc !important",
            "border": "2px solid #ffffff !important",
    },
    # 4. 테이블 모서리 둥글게
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