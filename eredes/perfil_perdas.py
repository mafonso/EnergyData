import pandas as pd
import os
from datetime import datetime, time

fileurl = r'https://www.e-redes.pt/sites/eredes/files/2023-01/E-REDES_Perfil_Perdas_2023.xlsx'

def load_perfil_perdas(source: str = fileurl):
    if not os.path.exists(source):
        source = fileurl

    print(f"Reading usage profiles from {source}")

    perfil_perdas = pd.DataFrame(
        columns=['bt', 'mt', 'at', 'atrt', 'mat'],
        index=pd.to_datetime([])
    )

    perfil = pd.read_excel(source, skiprows=4)
    for index, row in perfil.iterrows():
        date = perfil.iloc[index, 0]

        # ERSE uses 24:00 to denote midnight, we need to convert it to 00:00 plus one day
        if perfil.iloc[index, 2] == '24:00':
            perfil.iloc[index, 2] = '00:00'
            date = date + pd.DateOffset(days=1)
            time = datetime.strptime("00:00", '%H:%M').time()
        else:
            time = datetime.strptime(perfil.iloc[index, 2], '%H:%M').time()

        dt = datetime.fromtimestamp(date.timestamp()) + pd.DateOffset(hours=time.hour, minutes=time.minute)

        bt = perfil.iloc[index, 3]
        mt = perfil.iloc[index, 4]
        at = perfil.iloc[index, 5]
        atrt = perfil.iloc[index, 6]
        mat = perfil.iloc[index, 7]

        perfil_perdas.loc[dt] = [bt, mt, at, atrt, mat]
    print("done.")
    return perfil_perdas
