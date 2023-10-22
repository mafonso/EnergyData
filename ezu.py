import pandas as pd
from datetime import datetime, time, timedelta
import numpy as np


def calc_cgs(row):
    cgs = (row['encargos_regulacao'] + row['encargos_restricoes_pdbf'] + row['encargos_restricoes_tempo_real'] + row[
        'desvio_ren']) / row['consumo_global']

    print(cgs)
    return cgs


# function to calculate perdas as (1+perda_atrt)*(1+perda_at)*(1+perda_mt)*(1+perda_bt)
def calc_perdas(row):
    perdas = (1 + row['perda_atrt']) * (1 + row['perda_at']) * (1 + row['perda_mt']) * (1 + row['perda_bt'])
    return perdas


ezu = pd.read_csv('data/ezu/20230927024605_2023-07-30_2023-08-29_32456.csv', encoding="ISO-8859-1",
                  skiprows=3, skipfooter=9, delimiter=';', quotechar='"', engine='python', decimal=',')

ezu_df = pd.DataFrame(columns=['encargos_regulacao',
                               'encargos_restricoes_pdbf',
                               'encargos_restricoes_tempo_real',
                               'desvio_ren',
                               'consumo_global',
                               'perda_bt',
                               'perda_mt',
                               'perda_at',
                               'perda_atrt'],
                      index=pd.to_datetime([]))

ezu.info()
for index, row in ezu.iterrows():
    date = datetime.strptime(row['Data PT'], '%Y-%m-%d')
    hour = row['Hora PT'].split('h')[0]
    minute = row['Minutos'].split(' - ')[1]
    date = date + timedelta(hours=int(hour), minutes=int(minute))

    encargos_regulacao = row['Encargos Banda Regulação (EUR)']
    encargos_restricoes_pdbf = row['Encargos com a Resolução de Restrições Técnicas ao PDBF (EUR)']
    encargos_restricoes_tempo_real = row['Encargos com a Resolução de Restrições Técnicas em Tempo Real (EUR)']
    desvio_ren = row['Desvio REN (EUR)']
    consumo_global = row['Consumo global REN (MWh)']
    perda_bt = row['Perda BT (%)']
    perda_mt = row['Perda MT (%)']
    perda_ar = row['Perda AT (%)']
    perda_atrt = row['Perda ATRT (%)']

    ezu_df.loc[date] = [encargos_regulacao,
                        encargos_restricoes_pdbf,
                        encargos_restricoes_tempo_real,
                        desvio_ren,
                        consumo_global,
                        perda_bt,
                        perda_mt,
                        perda_ar,
                        perda_atrt
                        ]

# print(ezu_df.info())
# print(ezu_df.describe())
# print(ezu_df.head())

print(calc_perdas(ezu_df.loc['2023-07-30 00:00':'2023-07-30 02:00']))

# print(ezu_df.loc['2023-07-30 00:00':'2023-07-30 02:00'].consumo_global.sum())
