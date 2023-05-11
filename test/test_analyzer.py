# import src.dataframe_analyzer as analyzer
import src.dataframe_analyzer as analyzer
import pandas as pd
import pytest
from os import getcwd, sep

@pytest.fixture
def init_dataset():
    fld_pth = ['data', 'input', 'iris.csv']
    pth = sep.join(fld_pth)
    return pd.read_csv(pth)


def test_load_init_csv(init_dataset):
    # fld_pth = ['data', 'input', 'iris.csv']
    # dt = pd.read_csv(sep.join(fld_pth))
    assert type(init_dataset) == pd.DataFrame
    assert init_dataset.shape == (150, 5)

def test_load_dataframe_csv():
    fld_pth = ['data', 'input', 'iris.csv']
    dt = analyzer.load_data_csv(sep.join(fld_pth))
    assert type(dt) == pd.DataFrame
    assert dt.shape == (150, 5)
    assert list(dt.columns) == ["sepal length","sepal width","petal length","petal width","class"]

def test_validate_path():
    fld_pth = ['data', 'input']
    assert True == analyzer.validate_path(sep.join(fld_pth))