class Color:
    F0_BG = "#d7f0bd"
    F1_BG = "#ffd3a7"
    F2_BG = "#fff5b1"

    MAP_MAIN = "#0069e3" # 파란색
    MAP_BASIC = "#E0E0E0" # 연한 회색

    TABLE_BG = "#d1e0fc" # 하늘색

    DATE_TEXT = "#1B1B1B" # 진한 회색
    BASIC_TEXT = "#333333" # 회색
    MAP_BG = "#ffffff" # 더 연한 회색

    SECTION_BG = "#e9e9e9" # 더더 연한 회색
    TABLE_BG = "#f5f5f5" # 더더더 연한 회색

class Button:
    btn_back_style = {
        "color_scheme": "gray",
        "variant": "outline",
        "color": Color.BASIC_TEXT,
        "font_weight": "bold",
        "margin": "20px"
    }

    btn_chart_style = {
        "font_size": "17px",
        "font_weight": "bold",
        "color": Color.BASIC_TEXT,
        "width": "100%",
        "height": "55px",
        "margin_top": "15px",
        "margin_left": "15px"
    }

    btn_bar_chart_style = {
        **btn_chart_style,
        "transition": "all 0.2s ease-in-out",
        "_active": {"transform": "translateY(1px)"},
        "_hover": {"transform": "scale(1.05)", "color": "black"}
    }

    btn_main_bar_chart_style = {
        "font_size": "14px",
        "font_weight": "bold",
        "color": Color.BASIC_TEXT,
        "width": "90%",
        "height": "55px",
        "transition": "all 0.2s ease-in-out",
        "_active": {"transform": "translateY(1px)"},
        "_hover": {"transform": "scale(1.05)", "color": "black"}
    }

    btn_pie_chart_style = {
        **btn_chart_style,
        "bg": Color.F2_BG,
        "cursor": "default",
        "disabled": True,
        "_hover": {"bg": "#fff5b1"},
        "_active": {"bg": "#fff5b1"}
    }

class Text:
    # button text
    F0 = "신청 및 연계 현황"
    MAIN_FO_1 = "신청 및",
    MAIN_FO_2 = "연계 현황",
    F1 = "퇴원 환자 지원 현황"
    F2 = "자원 현황"
    BACK = "← 이전"

    # date(발췌일자) text
    F0_DATE = "* 발췌일자: 2026.1.12. / 예산지원형: 2025.2.17.~2026.1.9., 기술지원형: 2025.7.14~2026.1.9. 접수일 기준"
    F1_DATE = "* 발췌일자: 2025.12.31."
    F2_DATE = "* 발췌일자: 2025.12.1."

    TWO_LINE_TEXT = {
        "font_size": "14px",
        "font_weight": "bold",
        "line_height": "1.2"
    }
    TWO_LINE_CONTAINER = {
        "spacing": "0",
        "align_items": "center",
        "justify": "center",
        "width": "100%"
    }

class Config:
    # F0, F1, F2 버튼
    F0_CONFIG = {
        "title": Text.F0,
        "bg_color": Color.F0_BG
    }
    F1_CONFIG = {
        "title": Text.F1,
        "bg_color": Color.F1_BG
    }
    F2_CONFIG = {
        "title": Text.F2,
        "bg_color": Color.F2_BG
    }

class Chart:
    CHART_WRAPPER = {
        "align_items": "center",
        "width": "60%", # 차트 화면 비율
        "height": "100%",
        "overflow": "flex",
        "z_index": "1"
    }
    CHART_BUTTON_WRAPPER = {
        "width": "200px",
        "min_width": "200px",
        "margin_right": "13px"
    }
    TABLE_WRAPPER = {
        "width": "100%",
        "flex": "1",
        "overflow": "auto",
        "margin_top": "10px",
        "margin_right": "15px"
    }
    BAR_CHART_WRAPPER = {
        "width": "100%",
        "height": "100%",
        "padding": "20",
        "flex": "1",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "overflow": "auto",
        "style": {
            "zoom": "0.95"
        }
    }
    PIE_CHART_WRAPPER = {
        "flex": "1",
        "overflow": "auto"
    }
    TABLE = {
        "size": "1",
        "width": "100%"
    }
    # 파이를 나열하는 그리드
    PIE_CHART_GRID = {
        "wrap": "wrap",
        "spacing": "0",
        "justify": "center"
    }
    # 파이 하나를 감싸는 박스
    PIE_BOX = {
        "width": "320px",
        "min_width": "320px",
        "height": "300px",
        "margin": "0px",
        "overflow": "hidden"
    }
    PIE_PLOT = {
        "displayModeBar": False,
        "use_resize_handler": True
    }
    BAR_CHART_PLOT = {
        "use_resize_handler": True,
        "width": "100%",
        "height": "90%",
    }

class Date:
    TEXT = {
        "font_size": "16px",
        "color": Color.BASIC_TEXT,
        "font_weight": "bold",
        "text_align": "left",
        "width": "100%",
        "padding_left": "5px",
        "margin_left": "10px",
        "margin_top": "-10px"
    }

class Title:
    REGION = {
        "size": "6",
        "font_weight": "bold",
        "color": "black",
        "padding_top": "20px",
        "padding_bottom": "10px"
    }

class Map:
    MAP_PATH = {
        "stroke": "white",
        "stroke_width": "1",
        "transition": "all 0.2s ease",
        "_hover": {
            "fill": "#787878",
            "cursor": "pointer",
            "stroke": "black"
        }
    }

    MAP_CONTAINER = {
        "width": "100%",
        "height": "100%",
        "padding_left": "100px",
        "padding_top": "80px",
        # SVG 속성
        "preserveAspectRatio": "xMidYMid meet",
        "viewBox": "-1500 -1000 5000 3000"
    }

    MAP_BOX_WRAPPER = {
        "width": "40%", # 지도 화면 비율
        "height": "100vh",
        "bg": Color.MAP_BG,
        "position": "relative",
        "z_index": "999"
    }

class Table:
    # main 테이블 공통 헤더
    HEADER_CELL = {
        "vertical_align": "middle",
        "text_align": "center",
        "border_right": "2px solid #ffffff", # 오른쪽 테두리
        "border_bottom": "2px solid #ffffff" # 아래쪽 테두리
    }

    # main 테이블 소분류
    SUB_HEADER_CELL = {
        **HEADER_CELL,
        "font_size": "0.9em",
        "border_bottom": "none"
    }

    # (구분) 칸: 구분
    SECTION_CELL = {
        **HEADER_CELL,
        "bg": Color.SECTION_BG,
        "row_span": 2 # (구분) 칸: 대분류, 소분류 행을 합침
    }

    # main 테이블 행(row) 공통
    ROW = {
        "height": "37px",
        "align": "center",
        "_hover": {"bg": Color.TABLE_BG}
    }

    # main 테이블 데이터 셀
    DATA_CELL = {
        "text_align": "right",
        "border_right": f"1.5px solidv {Color.TABLE_BG}"
    }

    # main 테이블 (구분) 셀: 서울, 경기 등
    SECTION_LABEL_CELL = {
        "text_align": "center",
        "border_right": "1.5px solid #E2E2E2",
        "vertical_align": "middle"
    }

    # main 테이블 구조
    HEADERS = [
        {
            "title": "1) 신청 및 연계 현황(명)",
            "bg": "#d7f0bd",
            "columns": ["신청자", "통합판정완료", "서비스연계"]
        },
        {
            "title": "2) 자원 현황(건)",
            "bg": "#fff5b1",
            "columns": ["보건의료", "장기요양", "생활지원", "주거지원", "자체사업"]
        },
        {
            "title": "3) 퇴원환자 지원 현황(개, %, 건)",
            "bg": "#ffd3a7",
            "columns": ["요양병원수", "관외환자 입원율", "자원연계건수"]
        }
    ]

    # 강조할 행
    HIGHLIGHT_KEYWORD = "전국"

    LABEL_COLUMN_KEY = "구분_Unnamed: 0_level_1"
    DATA_COLUMN_KEYS = [
        # 신청 및 연계
        "신청 및 연계 현황 (명)_신청자",
        "신청 및 연계 현황 (명)_통합판정완료",
        "신청 및 연계 현황 (명)_서비스연계",

        # 자원 현황
        "자원 현황 (건)_보건의료",
        "자원 현황 (건)_장기요양",
        "자원 현황 (건)_생활지원",
        "자원 현황 (건)_주거지원",
        "자원 현황 (건)_자체사업",

        # 퇴원환자
        "퇴원환자 지원 현황 (개, %, 건)_요양병원수",
        "퇴원환자 지원 현황 (개, %, 건)_관외환자 입원율",
        "퇴원환자 지원 현황 (개, %, 건)_자원연계건수"
    ]
