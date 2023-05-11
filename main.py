import os
import src.dataframe_analyzer as analyzer
from src.dataframe_analyzer import DatumPydantic

# percorso completo con il nome del dataset da caricare come ultimo elemento
lst_folder = ['data', 'input', 'iris.csv']
df_path = os.sep.join(lst_folder)

# percorso completo con il nome del file di statistiche da salvare come ultimo elemento
stats_list_param = ['data', 'output', 'iris_stats.json']
stats_path = os.sep.join(stats_list_param[:-1])

dtantic = DatumPydantic()
dtantic.dataset = analyzer.load_data_csv(df_path)

print(f'DatAntic: {dtantic.categorical_attributes}')

diz = analyzer.get_stats(dtantic)

analyzer.change_values(diz, dtantic)
analyzer.save_data_stats(diz, stats_path, stats_list_param[-1])
analyzer.save_dataframe_as_csv(dtantic.dataset, stats_path, 'pippo.csv')