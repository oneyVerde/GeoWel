import reflex as rx
import plotly.express as px
import pandas as pd
from .processor import run_preprocessing
from .processor import get_table_data
from .processor import get_pie_data
from .processor import parse_svg_map
from .processor import get_choropleth_colors
from .processor import get_main_table
import plotly.graph_objects as go
from typing import Any, Dict

class State(rx.State):
    # 한글명
    REGION_MAPPING: dict = {
        "seoul": "서울특별시",
        "busan": "부산광역시",
        "daegu": "대구광역시",
        "incheon": "인천광역시",
        "gwangju": "광주광역시",
        "daejeon": "대전광역시",
        "ulsan": "울산광역시",
        "sejong": "세종특별자치도",
        "gyeonggi": "경기도",
        "gangwon": "강원특별자치도",
        "north-chungcheong": "충청북도",
        "south-chungcheong": "충청남도",
        "north-jeolla": "전북특별자치도",
        "south-jeolla": "전라남도",
        "north-gyeongsang": "경상북도",
        "south-gyeongsang": "경상남도",
        "jeju": "제주특별자치도"
    }

    region_name_code = {
        "서울특별시": 11.0,
        "부산광역시": 26.0,
        "대구광역시": 27.0,
        "인천광역시": 28.0,
        "광주광역시": 29.0,
        "대전광역시": 30.0,
        "울산광역시": 31.0,
        "경기도": 41.0,
        "충청북도": 43.0,
        "충청남도": 44.0,
        "전라남도": 46.0,
        "경상북도": 47.0,
        "경상남도": 48.0,
        "제주특별자치도": 50.0,
        "세종특별자치도": 36.0,
        "전북특별자치도": 52.0,
        "강원특별자치도": 51.0
    }

    # map 데이터
    map_paths: list[dict] = []
    area_names: list[str] = []
    base_color_map: Dict[float, str] = {}

    # svg 비율
    map_view_box: str = "0 0 100 100"

    # map 선택
    selected_region_kr: str = ""
    selected_region_code: float = 0.0

    # 상태 관리: main, f0, f1
    current_view: str = "main"

    # main 데이터
    main_data: list[dict] = []
    main_columns: list = []

    # 차트
    f0_table_data: list[dict] = []
    f1_table_data: list[dict] = []
    f2_pie_figs: list[go.Figure] = []
    f0_bar_fig: go.Figure = go.Figure()
    f1_bar_fig: go.Figure = go.Figure()

    f0_columns: list[str] = []
    f1_columns: list[str] = []

    # 프라이빗 변수
    _f0_df: pd.DataFrame = None
    _f1_df: pd.DataFrame = None
    _f2_total_raw_obj: Any = None
    _f2_raw_obj: Any = None
    _f0_date: str = "-"
    _f1_date: str = "-"
    f2_date: str = "-"

    is_loaded: bool = False

    def load_excel_data(self):
        file_path = "assets/service.xlsx"

        f0, f1, f2, f2_total, area_code, f0_date, f1_date, f2_date = run_preprocessing(file_path)

        self._f0_df = f0.df
        self._f1_df = f1.df
        self._f2_raw_obj = f2
        self._f2_total_raw_obj = f2_total

        self.f0_columns = f0.cat
        self.f1_columns = f1.cat

        self._f0_date = f0_date
        self._f1_date = f1_date
        self.f2_date = f2_date

        self.base_color_map = get_choropleth_colors(
            self._f0_df,
            key_col='시도코드',
            value_col='서비스연계율'
        )

        self.update_map_style()

        self.area_names = area_code['시도명'].tolist()

        self.selected_region_kr = ""
        self.selected_region_code = 0.0

        self.load_main_data()
        self.current_view = "main"

        self.is_loaded = True

    def load_map_data(self):
        map_file_path = "assets/map.svg"
        view_box, paths = parse_svg_map(map_file_path)
        self.map_view_box = view_box
        self.map_paths = paths
        for p in self.map_paths:
            p_id = p['id'].lower()
            p['name_kr'] = self.REGION_MAPPING.get(p_id, p['name'])

    def load_main_data(self):
        file_path = "assets/layout.xlsx"
        self.main_data, self.main_columns = get_main_table(file_path)

    def handle_map_click(self, item: dict):
        clicked_id = item['id'].lower()
        clicked_korean_name = self.REGION_MAPPING.get(clicked_id, item['name'])

        if self.selected_region_kr == clicked_korean_name:
            self.set_area("")
        else:
            self.set_area(clicked_korean_name)

    # 차트 생성 및 초기화
    def set_area(self, region_name: str):
        self.selected_region_kr = region_name

        if not region_name:
            self.selected_region_code = 0.0
            self.f0_table_data = []
            self.f1_table_data = []
            self.f2_pie_figs = []
            self.f0_bar_fig = go.Figure()
            self.f1_bar_fig = go.Figure()
            self.current_view = "main"
            self.update_map_style()
            return

        target_code = self.region_name_code.get(region_name)
        if target_code is None:
            print(f"'{region_name}'에 해당하는 시도코드를 찾을 수 없습니다.")
            self.selected_region_code = 0.0
            self.update_map_style()
            return

        self.selected_region_code = target_code

        # f2 인덱스
        target_index = self.area_names.index(region_name)
        if target_code is not None:
            self.draw_f0_table(target_code)
            self.draw_f1_table(target_code)
            self.draw_pie_chart(target_index)

        self.update_map_style()
        self.current_view = "main"

    # map 스타일
    def update_map_style(self):
        SELECTED_COLOR = "#0069e3"
        DEFAULT_GRAY = "#E0E0E0"

        new_paths = []
        for item in self.map_paths:
            # ID 매칭
            item_id = item['id'].lower()
            kr_name = self.REGION_MAPPING.get(item_id, item['name'])

            raw_code = self.region_name_code.get(kr_name, 0.0)
            my_code = int(raw_code)
            selected_code_int = int(self.selected_region_code)

            my_data_color = self.base_color_map.get(raw_code, DEFAULT_GRAY)

            # [2] 상황별 색상 결정
            if self.selected_region_code == 0.0:
                fill_color = my_data_color
            else:
                # Case B: 무언가 선택됨
                if my_code != 0 and my_code == selected_code_int:
                    fill_color = SELECTED_COLOR
                else:
                    fill_color = DEFAULT_GRAY

            new_item = item.copy()
            new_item['fill'] = fill_color
            new_paths.append(new_item)

        self.map_paths = new_paths

    # 토글
    def toggle_f0_chart(self):
        if self.current_view == "f0":
            self.current_view = "main"
        else:
            self.draw_f0_bar_chart(self.selected_region_code)
            self.current_view = "f0"

    def toggle_f1_chart(self):
        if self.current_view == "f1":
            self.current_view = "main"
        else:
            self.draw_f1_bar_chart(self.selected_region_code)
            self.current_view = "f1"

    def toggle_f2_chart(self):
        if self.current_view == "f2":
            self.current_view = "main"
        else:
            self.draw_pie_chart(self.selected_region_code, 320, 300, 13)
            self.current_view = "f2"

    # f0 표
    def draw_f0_table(self, target_code):
        if self._f0_df is not None:
            self.f0_table_data = get_table_data(self._f0_df, target_code)

    # f1 표
    def draw_f1_table(self, target_code):
        if self._f1_df is not None:
            self.f1_table_data =get_table_data(self._f1_df, target_code)

    # f0 막대 그래프
    def draw_f0_bar_chart(self, target_code):
        if self._f0_df is None:
            return

        data = self._f0_df.copy()
        value_column = '서비스연계율'

        data[value_column] = (data[value_column] * 100).round(0)
        data['시도명_bold'] = data['시도명'].apply(lambda x: f"<b>{x}</b>")

        # 발췌일
        extract_date = self._f0_date
        extract_date = extract_date.replace('-', '.') + '.'

        highlight_color = '#d7f0bd'
        base_color = '#E0E0E0'

        if target_code is None or target_code == 0:
            base_color,  highlight_color = highlight_color, base_color

        # 색상
        colors = [
            highlight_color if code == target_code else base_color
            for code in data['시도코드']
        ]

        fig = px.bar(
            data,
            x='시도명_bold',
            y=value_column,
            text_auto='.1%'
        )

        fig.update_traces(
            marker_color=colors,
            marker_line_width=0,
            texttemplate='<b>%{y:,.0f}</b>',
            textposition='outside',
            textfont_size=14,
            cliponaxis=False,
            constraintext='none',
        )

        fig.update_layout(
            title=dict(
                text=f"<b>지역별 통합돌봄 서비스연계율 현황</b>",
                font=dict(size=30),
                x=0.5,
                pad=dict(b=20)
            ),
            plot_bgcolor='white',
            width=1100,
            height=800,
            bargap=0.3,
            xaxis_title=None,
            yaxis_title=None,
            title_x=0.5,
            # 발췌일, 단위
            margin=dict(b=100, t=120),
            annotations=[
                dict(
                    x=1,
                    y=0.96,
                    xref="paper",
                    yref="paper",
                    text=f"<b>(단위: %, 발췌일자: {extract_date})</b>",
                    showarrow=False,
                    font=dict(
                        size=17,
                        color="#1B1B1B"
                    ),
                    xanchor="right",
                    yanchor="bottom"
                )
            ],
            xaxis=dict(
                title=None,
                tickmode='linear',
                tickangle=0,
                range=[-0.8, len(data) - 0.2],
                ticks='outside',
                ticklen=15,
                tickcolor='white',
                tickfont=dict(
                    size=18,
                    family="Arial Black, sans-serif"
                )
            ),
            yaxis=dict(
                tickformat=',.0f',
                dtick=10,
                range=[0, 110],
                tickfont=dict(
                    size=14,
                    family="Arial Black, sans-serif"
                )
            ),
            font=dict(size=14)
        )

        self.f0_bar_fig = fig

    # f1 막대 그래프
    def draw_f1_bar_chart(self, target_code):
        if self._f1_df is None:
            return

        data = self._f1_df.copy()
        value_column = '자원연계건수'

        data['시도명_bold'] = data['시도명'].apply(lambda x: f"<b>{x}</b>")

        # 발췌일
        extract_date = self._f1_date
        extract_date = extract_date.replace('-', '.') + '.'

        highlight_color = '#ffd3a7'
        base_color = '#E0E0E0'

        if target_code is None or target_code == 0:
            base_color,  highlight_color= highlight_color, base_color

        max_val = data[value_column].max()

        colors = [
            highlight_color if code == target_code else base_color
            for code in data['시도코드']
        ]

        fig = px.bar(
            data,
            x='시도명_bold',
            y=value_column,
            #title=f"<b>지역별 퇴원환자 자원연계건수</b>",
            #text_auto=True
        )

        fig.update_traces(
            marker_color=colors,
            marker_line_width=0,
            texttemplate='<b>%{y}</b>',
            textposition='outside',
            textfont_size=14,
            cliponaxis=False,
            constraintext='none',
        )

        fig.update_layout(
            title=dict(
                text=f"<b>지역별 퇴원환자 자원연계건수</b>",
                font=dict(size=30),
                x=0.5,
                pad=dict(b=20)
            ),
            uniformtext=dict(mode=False),
            plot_bgcolor='white',
            height=800,
            bargap=0.3,
            xaxis_title=None,
            yaxis_title=None,
            title_x=0.5,
            # 발췌일, 단위
            margin=dict(b=100, t=120),
            annotations=[
                dict(
                    x=1,
                    y=0.96,
                    xref="paper",
                    yref="paper",
                    text=f"<b>(단위: 건, 발췌일자: 2025.12.31.)</b>",
                    showarrow=False,
                    font=dict(
                        size=17,
                        color="#1B1B1B"
                    ),
                    xanchor="right",
                    yanchor="bottom"
                )
            ],
            xaxis=dict(
                title=None,
                tickmode='linear',
                tickangle=0,
                range=[-0.8, len(data) - 0.2],
                ticks='outside',
                ticklen=15,
                tickcolor='white',
                tickfont=dict(
                    size=18,
                    family="Malgun Gothic, sans-serif"
                )
            ),
            yaxis=dict(
                title=None,
                range=[0, max_val * 1.15],
                tickfont=dict(
                    size=14,
                    family="Arial Black, sans-serif"
                )
            ),
            font=dict(size=14)
        )

        self.f1_bar_fig = fig

    # f2 파이차트
    def draw_pie_chart(self, index, w=320, h=300, fs=13):
        if self._f2_raw_obj is None:
            return
        if self.selected_region_code == 0.0:
            if self._f2_total_raw_obj is not None:
                raw_data_list = get_pie_data(self._f2_total_raw_obj, 0)
        else:
            raw_data_list = get_pie_data(self._f2_raw_obj, index)

        custom_colors = ['#C496E0', '#659AA6', '#F7BB39', '#CEF5B6', '#A3CCF0']

        new_figs = []

        for d in raw_data_list:
            sub_title_text = f"<b>{d['title']}</b><br><span style='font-size:15px;'>총 {d['total']:,}건</span>"

            fig = go.Figure(data=[go.Pie(
                labels=d["labels"],
                values=d["values"],
                hole=0.4,

                marker=dict(
                    colors=custom_colors,
                    line=dict(color='#ffffff', width=3)
                ),

                textposition='inside',
                textinfo='percent+value',
                texttemplate=f'<b><span style="font-size:{fs}px">%{{percent}}</span><br><span style="font-size:{fs}px">(%{{value:,.0f}})</span></b>',
                hovertemplate='%{label}<br>%{value:,.0f}건<extra></extra>',

                title={
                    'text': sub_title_text,
                    'position': 'top center',
                    'font': {'size': 17},
                    'font_weight': 'bold'
                },
                showlegend=True
            )])

            fig.update_layout(
                margin=dict(t=10, b=0, l=30, r=60),
                height=h,  # 기본 높이,
                width=w,

                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="center",
                    x=1.3,
                    font=dict(size=11),
                    font_weight="bold"
                ),
                font=dict(family="Malgun Gothic, AppleGothic, sans-serif"),
            )

            new_figs.append(fig)

        self.f2_pie_figs = new_figs

    @property
    def f2_date(self):
        return self._f2_date
