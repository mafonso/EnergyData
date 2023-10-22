import pandas as pd
from datetime import datetime, time

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = os.environ.get("INFLUXDB_TOKEN")
org = "hangas"
url = "http://172.16.15.223:8086"
bucket="erse"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)


write_api = write_client.write_api(write_options=SYNCHRONOUS)

# read excel file
perfil = pd.read_excel('data/E-REDES_Perfil_Consumo_2023.xlsx', skiprows=4)

for index, row in perfil.iterrows():
    date = perfil.iloc[index, 0]

# ERSE uses 24:00 to denote midnight, we need to convert it to 00:00 plus one day
    if perfil.iloc[index, 2] == '24:00':
        perfil.iloc[index, 2] = '00:00'
        date = date + pd.DateOffset(days=1)
        time = datetime.strptime("00:00", '%H:%M').time()
    else:
        time = datetime.strptime(perfil.iloc[index, 2], '%H:%M').time()

    btn_a = perfil.iloc[index, 3]
    btn_b = perfil.iloc[index, 4]
    btn_c = perfil.iloc[index, 5]
    ip = perfil.iloc[index, 6]

    dt = datetime.fromtimestamp(date.timestamp()) + pd.DateOffset(hours=time.hour, minutes=time.minute)

    point = (
        Point("perfil")
        .time(dt)
        .field("btn_a", btn_a)
        .field("btn_b", btn_b)
        .field("btn_c", btn_c)
        .field("ip", ip)
    )

    if index % 1000 == 0: print (point.to_line_protocol())

    write_api.write(bucket=bucket, org="hangas", record=point)
    write_api.flush()

write_client.close()