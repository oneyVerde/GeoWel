import pytest
from unittest.mock import MagicMock
import pandas as pd
from GeoWel.processor import tree_cat, dataStr, \
    preprocessing_0_req_data, preprocessing_1_leave_data, \
    preprocessing_2_resource_data, run_preprocessing, \
    get_table_data, get_pie_data

def test_tree_cat():
    # 1) 부모-자식 관계가 리스트로 잘 묶이는 지
    # 2) Unnamed 컬럼이 제거 되는 지
    # 3) '계' 컬럼이 제거 되는 지

    # MultiIndex DataFrame
    columns = pd.MultiIndex.from_tuples(
        [
            ('A', 'Item1'),
            ('A', 'Item2'),
            ('A', '계'),
            ('B', 'Item1'),
            ('B', 'Item3'),
            ('Unnamed: 2', 'NaN'), # 병합된 셀
            ('A', 'Unnamed: 1')
        ]
    )
    df = pd.DataFrame(columns=columns)
    result = tree_cat(df)
    
    # then: A는 Item1, Item2만 / B는 Item1, Item3만
    excpt_a = ['A', ['Item1', 'Item2']]
    excpt_b = ['B', ['Item1', 'Item3']]

    # 1)
    assert excpt_a in result
    assert excpt_b in result

    # 2) 3)
    for p, c in result:
        assert '계' not in c
        assert 'Unnamed' not in str(p)


@pytest.fixture()
def mock_excel_file():
    ef = MagicMock()
    ef.sheet_names = ["Sheet1", "Sheet2", "Sheet3"]
    return ef


def test_preprocessing_0_req_data(mocker, mock_excel_file):
    # 1) NaN 행이 제거 되는 지
    # 2) col 0이 잘렸는 지
    # 3) dataStr에 데이터가 담기는 지
    # 4) sheet 명이 Sheet1로 매핑 되는 지
    # 5) 컬럼명이 dataStr.cat에 담기는 지

    test_df = pd.DataFrame(
        {
            "Col0": ["del", "del", "del"],
            "Col1": ["val1", None, "val2"],
            "Col2": [10, 20, 30]
        }
    )
    mock_read_excel = mocker.patch("GeoWel.processor.pd.read_excel")
    mock_read_excel.return_value = test_df
    
    # then: dataStr 객체
    result = preprocessing_0_req_data("test.xlsx", mock_excel_file)

    # 1)
    assert len(result.df) == 2

    # 2)
    assert "Col0" not in result.data.columns
    assert "Col1" in result.data.columns

    # 3)
    assert isinstance(result, dataStr)

    # 4)
    assert result.sheet_name == "Sheet1"

    # 5)
    assert result.cat == ["Col2"]


def test_preprocessing_1_leave_data(mocker, mock_excel_file):
    # 1) NaN 행이 제거 되는 지
    # 2) col 0이 잘렸는 지
    # 3) dataStr에 데이터가 담기는 지
    # 4) sheet 명이 Sheet3로 매핑 되는 지
    # 5) 컬럼명이 dataStr.cat에 담기는 지

    test_df = pd.DataFrame(
        {
            "Col0": ["del", "del", "del"],
            "Col1": ["val1", None, "val2"],
            "Col2": [10, 20, 30]
        }
    )
    mock_read_excel = mocker.patch("GeoWel.processor.pd.read_excel")
    mock_read_excel.return_value = test_df

    # then: dataStr 객체
    result = preprocessing_1_leave_data("test.xlsx", mock_excel_file)

    # 1)
    assert len(result.df) == 2

    # 2)
    assert "Col0" not in result.data.columns
    assert "Col1" in result.data.columns

    # 3)
    assert isinstance(result, dataStr)

    # 4)
    assert result.sheet_name == "Sheet3"

    # 5)
    assert result.cat == ["Col2"]


def test_preprocessing_2_resource_data(mocker, mock_excel_file):
    # 1) NaN 행이 제거 되는 지
    # 2) col 0, col 1이 잘렸는 지
    # 3) dataStr에 데이터가 담기는 지
    # 4) sheet 명이 Sheet2로 매핑 되는 지
    # 5) 컬럼명이 dataStr.cat에 담기는 지
    # 6) 데이터가 MultiIndex header=[0,1]으로 호출되었는 지

    test_df = pd.DataFrame(
        {
            "Col0": ["del", "del", "del"],
            "Col1": ["del", "del", "del"],
            "Col2": ["val1", None, "val2"],
            "Col3": [10, 20, 30]
        }
    )

    # then: dataStr 객체
    mock_read_excel = mocker.patch("GeoWel.processor.pd.read_excel")
    mock_read_excel.return_value = test_df

    mock_tree_cat = mocker.patch("GeoWel.processor.tree_cat")
    mock_tree_cat.return_value = ["MockedCategory"]

    result = preprocessing_2_resource_data("test.xlsx", mock_excel_file)

    # 1)
    assert len(result.df) == 2

    # 2)
    assert "Col0" not in result.data.columns
    assert "Col1" not in result.data.columns
    assert "Col2" in result.data.columns

    # 3)
    assert isinstance(result, dataStr)

    # 4)
    assert result.sheet_name == "Sheet2"

    # 5)
    assert result.cat == ["MockedCategory"]

    # 6)
    mock_read_excel.assert_called_with("test.xlsx", sheet_name=1, header=[0, 1])


def test_run_preprocessing(mocker):
    # 1) 엑셀 파일 객체가 생성 되는 지
    # 2) read_excel 호출 되는 지
    # 3) 각 함수가 올바른 인자로 호출 되는 지
    # 4) 날짜를 0, 1, 2의 인자로 호출 되는 지
    # 5) 리턴 값의 튜플 순서가 알맞은 지

    mock_ef = mocker.patch("GeoWel.processor.pd.ExcelFile")
    mock_read_excel = mocker.patch("GeoWel.processor.pd.read_excel")

    mock = {
        "f0": mocker.patch("GeoWel.processor.preprocessing_0_req_data", return_value="res_f0"),
        "f1": mocker.patch("GeoWel.processor.preprocessing_1_leave_data", return_value="res_f1"),
        "f2": mocker.patch("GeoWel.processor.preprocessing_2_resource_data", return_value="res_f2"),
        "f2_total": mocker.patch("GeoWel.processor.get_f2_total_data", return_value="res_f2_total"),
        "date": mocker.patch("GeoWel.processor.get_date", side_effect=["d0", "d1", "d2"])
    }

    # then: 1)의 튜플
    result = run_preprocessing("test.xlsx")
    
    # 1)
    mock_ef.assert_called_once_with("test.xlsx")

    # 2)
    mock_read_excel.assert_called_once_with("test.xlsx", sheet_name=3)

    # 3)
    mock["f0"].assert_called_once_with("test.xlsx", mock_ef.return_value)
    mock["f1"].assert_called_once_with("test.xlsx", mock_ef.return_value)
    mock["f2"].assert_called_once_with("test.xlsx", mock_ef.return_value)
    mock["f2_total"].assert_called_once_with("test.xlsx")

    # 4)
    assert mock["date"].call_count == 3
    assert mock["date"].call_args_list[0] == mocker.call("test.xlsx", 0)
    assert mock["date"].call_args_list[1] == mocker.call("test.xlsx", 1)
    assert mock["date"].call_args_list[2] == mocker.call("test.xlsx", 2)

    # 5)
    assert result == (
        "res_f0",
        "res_f1",
        "res_f2",
        "res_f2_total",
        mock_read_excel.return_value, # area_code
        "d0",
        "d1",
        "d2"
    )


def test_get_table_data():
    # 1) 리스트를 반환하는 지
    # 2) 타겟 시도코드에 해당하는 데이터만 추출되는 지
    # 3) 불필요한 "시도코드" 컬럼이 제거 되는 지
    # 4) 데이터 포맷팅: 퍼센트는 00.0%, 세자리수 콤마
    # 5) 타겟 시도코드가 없을 경우 빈 리스트를 반환하는 지

    test_df = pd.DataFrame(
        {
            "시도코드": [11.0, 26.0],
            "지역명": ["서울", "부산"],
            "연계율": [0.555, None],
            "건수": [1000, 2000]
        }
    )

    # then: list of dictionary
    result = get_table_data(test_df, 11.0)

    # 1)
    assert isinstance(result, list)

    row = result[0]

    # 2)
    assert row["지역명"] == "서울"

    # 3)
    assert "시도코드" not in row

    # 4)
    assert row["연계율"] == "55.5%"
    assert row["건수"] == "1,000"

    # 5)
    none_res = get_table_data(test_df, 0.0)
    assert none_res == []


def test_get_pie_data(mocker):
    # 1) 리스트를 반환하는 지
    # 2) "구분", "시/도" 등 불필요한 컬럼이 제거 되는 지
    # 3) 차트 제목과 라벨이 올바르게 매핑 되는 지
    # 4) 수치 데이터가 타겟 행에서 추출 되는 지
    # 5) "계" 컬럼은 Total 값을 분리 하는 지

    cols = pd.MultiIndex.from_tuples(
        [
            ("A", "항목1"),
            ("A", "항목2"),
            ("A", "계"),
            ("구분", "값")
        ]
    )

    test_df = pd.DataFrame(
        [
            [10, 5, 100, 8888],
            [20, 8, 200, 9999]
        ]
    , columns=cols)

    tree_cat_list = [
        ("A", ["항목1", "항목2"]),
        ("구분", ["값"])
    ]

    mock_data_str = mocker.Mock()
    mock_data_str.data = test_df
    mock_data_str.cat = tree_cat_list

    # then: chart list
    result = get_pie_data(mock_data_str, target=0)

    # 1)
    assert isinstance(result, list)

    # 2)
    assert len(result) == 1

    chart = result[0]

    # 3)
    assert chart["title"] == "A"
    assert chart["labels"] == ["항목1", "항목2"]

    # 4)
    assert chart["values"] == [10, 5]

    # 5)
    assert chart["total"] == 100

