import pandas as pd
from datetime import datetime, time, timedelta

import main

tarifasegura_tecto_simples = 0.1329
tarifasegura_chao_simples = 0.0729
tar = -0.0121


def calc_cgs(row):
    cgs = (row['encargos_regulacao'] + row['encargos_restricoes_pdbf'] + row['encargos_restricoes_tempo_real'] + row[
        'desvio_ren']) / row['consumo_global']
    return cgs


def calc_perdas(row):
    perdas = (1 + row['perda_atrt']) * (1 + row['perda_at']) * (1 + row['perda_mt']) * (1 + row['perda_bt'])
    return perdas

def calc_price(row):
    price = (row['preco_omie'] + calc_cgs(row) + row['k']) * calc_perdas(row)
    return price.clip(lower=tarifasegura_chao_simples*1000, upper=tarifasegura_tecto_simples*1000)

def calc_cost(row):
    cost = calc_price(row) * row['curva_carga'] + (tar * row['curva_carga'] * 1000)
    return cost

ezu = pd.read_csv('data/ezu/20231002173951_2023-08-30_2023-09-29_32083.csv', encoding="ISO-8859-1", skiprows=3,
                  skipfooter=9, delimiter=';', quotechar='"', engine='python', decimal=',')

ezu_df = pd.DataFrame(
    columns=['encargos_regulacao', 'encargos_restricoes_pdbf', 'encargos_restricoes_tempo_real', 'desvio_ren',
             'consumo_global', 'perda_bt', 'perda_mt', 'perda_at', 'perda_atrt', 'preco_omie', 'k', 'curva_carga', ],
    index=pd.to_datetime([]))

#print(ezu_df.info())

for index, row in ezu.iterrows():
    date = datetime.strptime(row['Data PT'], '%Y-%m-%d')
    hour = row['Hora PT'].split('h')[0]
    minute = row['Minutos'].split(' - ')[1]
    date = date + timedelta(hours=int(hour), minutes=int(minute))

    # CGS
    encargos_regulacao = row['Encargos Banda Regulação (EUR)']
    encargos_restricoes_pdbf = row['Encargos com a Resolução de Restrições Técnicas ao PDBF (EUR)']
    encargos_restricoes_tempo_real = row['Encargos com a Resolução de Restrições Técnicas em Tempo Real (EUR)']
    desvio_ren = row['Desvio REN (EUR)']
    consumo_global = row['Consumo global REN (MWh)']

    # perdas
    perda_bt = row['Perda BT (%)']
    perda_mt = row['Perda MT (%)']
    perda_ar = row['Perda AT (%)']
    perda_atrt = row['Perda ATRT (%)']

    # OMIE
    preco_omie = row['Preço aquisição OMIE (EUR/MWh)']
    k = row['K (EUR/MWh)']

    # Consumos
    cuva_carga = row['Curva carga perfilada (MWh)']

    ezu_df.loc[date] = [encargos_regulacao, encargos_restricoes_pdbf, encargos_restricoes_tempo_real, desvio_ren,
                        consumo_global, perda_bt, perda_mt, perda_ar, perda_atrt, preco_omie, k, cuva_carga]

# print(ezu_df.info())
# print(ezu_df.describe())
# print(ezu_df.head())

# print(calc_perdas(ezu_df.loc['2023-07-30 00:00':'2023-07-30 02:00']))


ezu_slice = ezu_df.loc['2023-08-30 00:00':'2023-09-30 00:00']

print("Consumo :", '{:.0f}'.format(ezu_slice.curva_carga.sum()*1000))
print("Custo :", '{:.2f}'.format(calc_cost(ezu_slice).sum()))
print("Preço Medio kWh :", '{:.6f}'.format(calc_cost(ezu_slice).sum() / ezu_slice.curva_carga.sum() / 1000))


# convert the above to golang