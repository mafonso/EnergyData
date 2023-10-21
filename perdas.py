# import pandas lib as pd
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
perdas = pd.read_excel('data/perfis-de-perdas-2023.xls', skiprows=2)

for index, row in perdas.iterrows():
    date = perdas.iloc[index, 0]

# ERSE uses 24:00 to denote midnight, we need to convert it to 00:00 plus one day
    if perdas.iloc[index, 2] == '24:00':
        perdas.iloc[index, 2] = '00:00'
        date = date + pd.DateOffset(days=1)
        time = datetime.strptime("00:00", '%H:%M').time()
    else:
        time = datetime.strptime(perdas.iloc[index, 2], '%H:%M').time()

    bt = perdas.iloc[index, 3]
    mt = perdas.iloc[index, 4]
    at = perdas.iloc[index, 5]
    atrt = perdas.iloc[index, 6]
    mat = perdas.iloc[index, 7]

    dt = datetime.fromtimestamp(date.timestamp()) + pd.DateOffset(hours=time.hour, minutes=time.minute)

    point = (
        Point("perdas")
        .time(dt)
        .field("bt", bt)
        .field("mt", mt)
        .field("at", at)
        .field("atrt", atrt)
        .field("mat", mat)
    )

    if index % 1000 == 0: print (point.to_line_protocol())

    write_api.write(bucket=bucket, org="hangas", record=point)
    write_api.flush()

write_client.close()