import pandas as pd
import os
from datetime import datetime, time
from pytz import timezone

fileurl = r'https://www.e-redes.pt/sites/eredes/files/2023-01/E-REDES_Perfil_Consumo_2023.xlsx'

def load_perfil(source: str = fileurl):
    if not os.path.exists(source):
        source = fileurl

    perfil_consumo = pd.DataFrame(
        columns=['btn_a', 'btn_b', 'btn_c', 'ip'],
        index=pd.to_datetime([], utc=True))

    print(f"Reading usage profiles from {source}")
    file = pd.read_excel(source, skiprows=3)


    for index, row in file.iterrows():
        date = file.iloc[index, 0]
        # ERSE uses 24:00 to denote midnight, we need to convert it to 00:00 plus one day
        if file.iloc[index, 2] == '24:00':
            file.iloc[index, 2] = '00:00'
            date = date + pd.DateOffset(days=1)

        time = datetime.strptime(file.iloc[index, 2], '%H:%M').time()

        dt = datetime.fromtimestamp(date.timestamp(),timezone('UTC')) + pd.DateOffset(hours=time.hour, minutes=time.minute)

        btn_a = row['BTN A']
        btn_b = row['BTN B']
        btn_c = row['BTN C']
        ip = row['IP']

        perfil_consumo.loc[dt] = [btn_a, btn_b, btn_c, ip]

    print("done.")
    return perfil_consumo
