# import src.dataframe_analyzer as analyzer
import src.dataframe_analyzer as analyzer
import pandas as pd
import pytest
from os import sep

@pytest.fixture
def init_dataset():
    fld_pth = ['data', 'input', 'iris.csv']
    pth = sep.join(fld_pth)
    return pd.read_csv(pth)

@pytest.fixture
def init_datum():
    fld_pth = ['data', 'input', 'iris.csv']
    pth = sep.join(fld_pth)
    data = analyzer.DatumPydantic()
    data.dataset = pd.read_csv(pth)
    return data


def test_load_init_csv(init_dataset):
    # fld_pth = ['data', 'input', 'iris.csv']
    # dt = pd.read_csv(sep.join(fld_pth))
    assert type(init_dataset) == pd.DataFrame
    assert init_dataset.shape == (150, 5)

def test_load_dataframe_csv():
    fld_pth = ['data', 'input', 'iris.csv']
    dt = None
    assert dt == None
    dt = analyzer.load_data_csv(sep.join(fld_pth))
    assert type(dt) == pd.DataFrame
    assert dt.shape == (150, 5)
    assert list(dt.columns) == ['sepal length','sepal width','petal length','petal width','class']

def test_validate_path():
    fld_pth = ['data', 'input']
    assert True == analyzer.validate_path(sep.join(fld_pth))

def test_property_attributes(init_datum):
    cols = ['sepal length','sepal width','petal length','petal width','class']
    assert len(cols) == len(init_datum.attributes)
    for e in list(zip(cols,init_datum.attributes)):
        assert e[0] == e[1]

def test_property_categorical_attributes(init_datum):
    cols = ['class']
    assert len(cols) == len(init_datum.categorical_attributes)
    for e in list(zip(cols,init_datum.categorical_attributes)):
        assert e[0] == e[1]

def test_type_dataset_datum_class(init_datum):
    assert type(init_datum.dataset) == pd.DataFrame

def test_get_stats(init_datum):
    valid_dict = {
        "class": {
            "Iris-setosa": "[0, 50, 33.333333333333336]",
            "Iris-versicolor": "[1, 50, 33.333333333333336]",
            "Iris-virginica": "[2, 50, 33.333333333333336]"
            }
        }
    result = analyzer.get_stats(init_datum)
    # check if elements have the same keys lenghts
    assert len(valid_dict.keys()) == len(result.keys())
    assert len(valid_dict['class'].keys()) == len(result['class'].keys())

    # checks if each waited key has the same values
    assert valid_dict['class'] == result['class']
    assert valid_dict['class']['Iris-setosa'] == result['class']['Iris-setosa']
    assert valid_dict['class']['Iris-versicolor'] == result['class']['Iris-versicolor']
    assert valid_dict['class']['Iris-virginica'] == result['class']['Iris-virginica']
    
    # this solution is not good: in case of an error it will be more difficult
    # to find what is the value that has generated the error
    # for couple in zip(valid_dict['class'], result['class']):
    #     assert couple[0] == couple[1]
    #     assert valid_dict['class'][couple[0]] == result['class'][couple[1]]

def test_convert_attribute_to_categorical():
    ...