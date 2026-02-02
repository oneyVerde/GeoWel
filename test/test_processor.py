import pytest
from unittest.mock import MagicMock
import pandas as pd
from GeoWel.processor import tree_cat, dataStr, \
    preprocessing_0_req_data, preprocessing_1_leave_data, \
    preprocessing_2_resource_data

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

