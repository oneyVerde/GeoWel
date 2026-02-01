from . import components as CMP
from . import styles as STY

class Config:
    # F0, F1, F2 버튼
    F0_CONFIG = {
        "title": STY.Text.F0,
        "bg_color": STY.Color.F0_BG
    }
    F1_CONFIG = {
        "title": STY.Text.F1,
        "bg_color": STY.Color.F1_BG
    }
    F2_CONFIG = {
        "title": STY.Text.F2,
        "bg_color": STY.Color.F2_BG
    }

    # Main F0 버튼
    MAIN_F0_CONFIG = {
        "title": CMP.two_line_text(STY.Text.MAIN_FO_1, STY.Text.MAIN_FO_2),
        "bg_color": STY.Color.F0_BG
    }