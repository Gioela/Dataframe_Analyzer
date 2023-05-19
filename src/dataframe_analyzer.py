import pandas as pd
import numpy as np
import json
from pathlib import Path
from os import sep

class DatumPydantic:
    dataset: pd.DataFrame

    @property
    def attributes(self):
        return self.dataset.columns
    
    @property
    def categorical_attributes(self):
        return [col for col in self.dataset.columns if pd.api.types.is_object_dtype(self.dataset[col])]
        # self._categorical_attributes = [col for col in self.dataset.columns if pd.api.types.is_object_dtype(self.dataset[col])]
        # return self._categorical_attributes
    

class Datum:
    def __init__(self, data_pth: str):
        self.__setup(data_pth)

    def __setup(self, pth: str):
        self.dataset= load_data_csv(pth)

    @property
    def attributes(self):
        return self.dataset.columns()    

    @property
    def categorical_attributes(self):
        return [col for col in self.dataset.columns if pd.api.types.is_object_dtype(self.dataset[col])]


def get_stats(df: DatumPydantic, sort_details: bool = False) -> dict:
    result = dict()
    for col in df.categorical_attributes:
        col_det = df.dataset[col].value_counts(sort=sort_details, dropna=False)
        result[col] = {col_det.index[idx]: str([idx, col_det[idx], col_det[idx] * 100 / np.sum(col_det)] ) for idx in range(len(col_det.index))}
    # for k,v in result.items():
    #     print(k, v)
    return result

def convert_attribute_name_to_object_type(data: DatumPydantic, col_name: str, in_place: bool=True) -> None:
    try:
        if in_place:
            data.dataset = data.dataset.astype({col_name : 'object'})
        else:
            return data.dataset.astype({col_name : 'object'})
    except KeyError as e:
        # raise KeyError('column name is incorrect or not found')
        raise e

def change_values(converter: dict, data: DatumPydantic):
    for col_name in converter.keys():
        data.dataset[col_name].replace(to_replace=pd.unique( data.dataset[col_name] ),
                                        value=[ x.split()[0][1:-1] for x in converter[col_name].values()],
                                        inplace=True)
        data.dataset[col_name] = pd.to_numeric(data.dataset[col_name])

def validate_path(pth: str, parents: bool = True, exist: bool = True) -> bool:
    try:
        Path(pth).mkdir(parents=parents, exist_ok=exist)
        return True
    except Exception as e:
        raise e

def save_data_stats(data_stats: dict, pth: str, f_name: str):
    try:
        validate_path(pth=pth)
        with open(sep.join([pth, f_name]), 'w') as f:
            json.dump(data_stats, f)
        msg= 'File di statistiche salvato correttamente'
    except Exception as e:
        print(e)
        msg= 'Errore nel salvataggio'
    finally:
        print(msg)

def save_dataframe_as_csv(data: pd.DataFrame, pth: str, f_name: str, separator: chr = ',', decimal_separator: chr = '.'):
    try:
        validate_path(pth=pth)
        data.to_csv(path_or_buf=sep.join([pth, f_name]),
                    sep=separator, index=False,
                    decimal=decimal_separator)
        msg = 'Dataframe convertito salvato correttamente'
    except Exception as e:
        print(e)
        msg= 'Errore nel salvataggio del dataframe'
    finally:
        print(msg)

def load_data_csv(pth: str, separator: chr = ',', memoy: bool = False) -> pd.DataFrame:
    return pd.read_csv(pth, sep=separator, low_memory=memoy)

