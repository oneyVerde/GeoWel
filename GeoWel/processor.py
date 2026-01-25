import pandas as pd
import unicodedata
from dataclasses import dataclass
import re
import xml.etree.ElementTree as ET

@dataclass
class dataStr:
    sheet_name: str
    df: pd.DataFrame
    cat: list
    data: list

def tree_cat(data):
    cat = []
    for parent in data.columns.get_level_values(0).unique():
        if "Unnamed" in str(parent): continue
        children = [c for p, c in data.columns if p == parent and "Unnamed" not in str(c) and c != "계"]
        cat.append([parent, children])
    return cat

def preprocessing_0_req_data(file_path, ef):
    sheet_name = ef.sheet_names[0]
    df = pd.read_excel(file_path, sheet_name=0)
    df = df.dropna(subset=[df.columns[1]])
    data = df.iloc[:, 1:]
    cat = df.columns[2:].tolist()
    return dataStr(sheet_name=sheet_name, df=df, cat=cat, data=data)

def preprocessing_1_leave_data(file_path, ef):
    sheet_name = ef.sheet_names[2]
    df = pd.read_excel(file_path, sheet_name=2)
    df = df.dropna(subset=[df.columns[1]])
    data = df.iloc[:, 1:]
    cat = df.columns[2:].tolist()
    return dataStr(sheet_name=sheet_name, df=df, cat=cat, data=data)

def preprocessing_2_resource_data(file_path, ef):
    sheet_name = ef.sheet_names[1]
    df = pd.read_excel(file_path, sheet_name=1, header=[0,1])
    df = df.dropna(subset=[df.columns[2]])
    data = df.iloc[:, 2:]
    cat = tree_cat(data)
    return dataStr(sheet_name=sheet_name, df=df, cat=cat, data=data)

# State에서 호출할 통합 실행 함수
def run_preprocessing(file_path):
    ef = pd.ExcelFile(file_path)
    area_code = pd.read_excel(file_path, sheet_name=3)
    f0 = preprocessing_0_req_data(file_path, ef)
    f1 = preprocessing_1_leave_data(file_path, ef)
    f2 = preprocessing_2_resource_data(file_path, ef)
    f2_total = get_f2_total_data(file_path)
    f0_date = get_date(file_path, 0)
    f1_date = get_date(file_path, 1)
    f2_date = get_date(file_path, 2 )
    return f0, f1, f2, f2_total, area_code, f0_date, f1_date, f2_date

# table data
def get_table_data(data: pd.DataFrame, target_code):
    target_data = data[data['시도코드'] == target_code]
    if target_data.empty:
        return []

    result_df = target_data.iloc[:, 1:].copy()
    # % format (str로 변환)
    for col in result_df.columns:
        if '율' in col:
            numeric_series = pd.to_numeric(result_df[col], errors='coerce')

            result_df[col] = numeric_series.apply(
                lambda x: f"{x:.1%}" if pd.notnull(x) else "-"
            )

    result_df = comma_format(result_df)

    return result_df.to_dict("records")

# pie chart data
def get_pie_data(data_str, target=0):
    cat = data_str.cat
    data = data_str.data

    row = data.iloc[int(target)]
    charts = []

    for parent, children in cat:
        if parent in ['구분', '시/도', '시도코드', 'Unnamed: 0_level_0']:
            continue

        values = []
        labels = []
        for child in children:
            try:
                val = row[(parent, child)]
                values.append(val)
                labels.append(child)
            except KeyError:
                continue

        try:
            total = row[(parent, '계')]
        except KeyError:
            continue

        charts.append({
            "title": parent,
            "labels": labels,
            "values": values,
            "total": int(total)
        })

    return charts

def parse_svg_map(file_path: str):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        view_box = root.attrib.get("viewBox", "0 0 1771.626 1672.413")

        paths = []

        for i, elem in enumerate(root.iter()):
            tag_name = re.sub(r'\{.*\}', '', elem.tag)

            if tag_name == 'path':
                d_val = elem.attrib.get('d')

                if d_val:
                    region_id = elem.attrib.get('id', f"region_{i}")
                    region_name = elem.attrib.get('aria-label') or elem.attrib.get('name') or region_id

                    paths.append({
                        "id": region_id,
                        "name": region_id,
                        "d": d_val,
                        "fill": elem.attrib.get('fill', '#E0E0E0')
                    })
        return view_box, paths

    except Exception as e:
        print(f"SVG 파싱 오류: {e}")
        return "0 0 1771 1672", []


def get_region_code(file_path: str):
    df = pd.read_excel(file_path, sheet_name=3)

    region_names = df.iloc[:, 1].astype(str).apply(lambda x: unicodedata.normalize('NFC', x)).str.strip()
    region_codes = pd.to_numeric(df.iloc[:, 0], errors='coerce').fillna(0.0).astype(float)

    region_mapping = dict(zip(region_names, region_codes))

    return region_mapping

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_choropleth_colors(df: pd.DataFrame, key_col: str, value_col: str):
    START_COLOR = "#E0E0E0"
    END_COLOR = "#0069e3"

    df = df.copy()
    df[key_col] = pd.to_numeric(df[key_col], errors='coerce').fillna(0.0).astype(float)

    subset = df.dropna(subset=[value_col])
    min_val = subset[value_col].min()
    max_val = subset[value_col].max()

    start_rgb = hex_to_rgb(START_COLOR)
    end_rgb = hex_to_rgb(END_COLOR)

    color_map = {}

    for _, row in df.iterrows():
        code = row[key_col]
        val = row[value_col]

        if pd.isna(val):
            color_map[code] = "#E0E0E0"
            continue

        if max_val == min_val:
            ratio = 0.5
        else:
            ratio = (val - min_val) / (max_val - min_val)

        ratio = ratio**2

        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio

        color_map[code] = rgb_to_hex((r, g, b))

    return color_map

# 발췌일
def get_date(file_path, row: int = 0):
    data = pd.read_excel(file_path, sheet_name=4)
    result = data.loc[data['시트'] == row, '발췌일'].values[0]
    # 날짜 형식
    format_result = pd.to_datetime(result).strftime('%Y-%m-%d')
    return str(format_result)

# main 테이블
def get_main_table(file_path):
    df = pd.read_excel(file_path, header=[0,1])

    columns = []
    for col in df.columns:
        if "Unnamed" in col[0]:
            columns.append(col[1])
        else:
            columns.append(f"{col[0]}_{col[1]}")
    df.columns = columns

    df = comma_format(df)

    return df.to_dict("records"), columns

# 세자리 콤마
def comma_format(df):
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].apply(
                lambda x: f"{x:,.0f}" if pd.notnull(x) else ""
            )

    return df

# f2 자원 현황 파이차트 합계 데이터
def get_f2_total_data(file_path):
    df = pd.read_excel(file_path, sheet_name=5, header=[0,1])
    df = df.dropna(subset=[df.columns[2]])
    data = df.iloc[:, :]
    cat = tree_cat(data)
    return dataStr(sheet_name="6. 자원 현황 합계", df=df, cat=cat, data=data)