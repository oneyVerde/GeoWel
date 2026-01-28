class Color:
    F0_BG = "#d7f0bd"
    F1_BG = "#ffd3a7"
    F2_BG = "#fff5b1"

    MAP_MAIN = "#0069e3" # 파란색
    MAP_BASIC = "#E0E0E0" # 연한 회색

    TABLE_BG = "#d1e0fc" # 하늘색

    DATE_TEXT = "#1B1B1B" # 진한 회색
    BASIC_TEXT = "#333333" # 회색

class Button:
    btn_back_style = {
        "color_scheme": "gray",
        "variant": "outline",
        "color": Color.BASIC_TEXT,
        "font_weight": "bold"
    }

    btn_bar_chart_style = {
        "font_size": "17px",
        "color": Color.BASIC_TEXT,
        "font_weight": "bold",

        "width": "100%",
        "height": "55px",
        "transition": "all 0.2s ease-in-out",
        "_active": {"transform": "translateY(1px)"},
        "_hover": {"transform": "scale(1.05)", "color": "black"},

        "margin_top": "15px",
        "margin_left": "15px",
    }

    btn_pie_chart_style = {
        "font_size": "17px",
        "font_weight": "bold",

        "bg": Color.F2_BG,
        "color": Color.BASIC_TEXT,

        "width": "20%",
        "height": "55px",
        "cursor": "default",
        "disabled": "True",
        "_hover": {"bg": "#fff5b1"},
        "_active": {"bg": "#fff5b1"},

        "margin_left": "15px",
        "margin_top": "10px"

    }

class Text:
    # button text
    F0 = "신청 및 연계 현황"
    F1 = "퇴원 환자 지원 현황"
    F2 = "자원 현황"
    BACK = "← 이전"

    # date(발췌일자) text
    F0_DATE = "* 발췌일자: 1) 2026.1.12. / 예산지원형: 2025.2.17.~2026.1.9., 기술지원형: 2025.7.14~2026.1.9. 접수일 기준"
    F1_DATE = "* 발췌일자: 2025.12.31."
    F2_DATE = "* 발췌일자: 2025.12.1."

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

class Layout:
    BAR_CHART_BUTTON_WRAPPER = {
        "width": "20%",
        "min_width": "200px",
        "margin_right": "13px"
    }
    PIE_CHART_BUTTON_WRAPPER = {
        "width": "100%",
        "min_width": "200px",
        "text_align": "left",
        "padding_left": "20px",
        "margin_top": "10px"
    }
    TABLE_WRAPPER = {
        "flex": "1",
        "overflow": "auto",
        "margin_top": "10px",
        "margin_right": "15px"
    }

class Table:
    PROPS = {
        "size": "1",
        "width": "100%"
    }

class Date:
    TEXT = {
        "font_size": "16px",
        "color": Color.BASIC_TEXT,
        "font_weight": "bold",
        "text-align": "left",
        "width": "100%",
        "padding_left": "5px",
        "margin_left": "10px",
        "margin_top": "-10px"
    }