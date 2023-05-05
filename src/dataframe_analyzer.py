import os
import pandas as pd
import numpy as np
from pathlib import Path
import json

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
        self.dataset= load_csv(pth)

    @property
    def attributes(self):
        return self.dataset.columns()    

    @property
    def categorical_attributes(self):
        return [col for col in self.dataset.columns if pd.api.types.is_object_dtype(self.dataset[col])]


def get_details(df: DatumPydantic, sort_details: bool = False) -> dict:
    result = dict()
    for col in df.categorical_attributes:
        col_det = df.dataset[col].value_counts(sort=sort_details, dropna=False)
        result[col] = {col_det.index[idx]: str([idx, col_det[idx], col_det[idx] * 100 / np.sum(col_det)] ) for idx in range(len(col_det.index))}

    # for k,v in result.items():
    #     print(k, v)
    return result

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
        with open(os.sep.join([pth, f_name]), 'w') as f:
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
        data.to_csv(path_or_buf=os.sep.join([pth, f_name]),
                    sep=separator, index=False,
                    decimal=decimal_separator)
        msg = 'Dataframe convertito salvato correttamente'
    except Exception as e:
        print(e)
        msg= 'Errore nel salvataggio del dataframe'
    finally:
        print(msg)

def load_csv(pth: str, separator: chr = ',', memoy: bool = False) -> pd.DataFrame:
    return pd.read_csv(pth, sep=separator, low_memory=memoy)

# percorso completo con il nome del dataset da caricare come ultimo elemento
lst_folder = [...,'DF_NAME.csv']
df_path = os.sep.join(lst_folder)

# percorso completo con il nome del file di statistiche da salvare come ultimo elemento
stats_list_param = [..., 'STATS_FILE_NAME.json']
stats_path = os.sep.join(stats_list_param[:-1])

dtantic = DatumPydantic()
dtantic.dataset = load_csv(df_path)

print(f'DatAntic: {dtantic.categorical_attributes}')

diz = get_details(dtantic)

change_values(diz, dtantic)
save_data_stats(diz, stats_path, stats_list_param[-1])
save_dataframe_as_csv(dtantic.dataset, stats_path, 'pippo.csv')
